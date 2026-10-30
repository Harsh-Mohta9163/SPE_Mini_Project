pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5'))
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    triggers {
        // Trigger on GitHub Webhook push events; fallback to polling every 5 minutes
        githubPush()
        pollSCM('H/5 * * * *')
    }

    environment {
        // Application and Registry Configuration
        APP_NAME = 'calculator-api'
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE_NAME = 'harshmohta9163/calculator-api'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        
        // Jenkins Credentials Store ID (Configured in Jenkins -> Manage Credentials)
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-creds'
        
        // Notification settings
        NOTIFICATION_EMAIL = 'harshmohta9163@gmail.com'
        
        // Maven Configuration
        MAVEN_OPTS = '-Dorg.slf4j.simpleLogger.log.org.apache.maven.cli.transfer.Slf4jMavenTransferListener=warn'
        
        // Service verification URLs
        HEALTHCHECK_URL = 'http://localhost/actuator/health'
        SMOKE_TEST_URL = 'http://localhost/api/v1/add?a=10&b=20'
    }

    stages {
        // ----------------------------------------------------
        // Stage 1: Checkout Source Code
        // ----------------------------------------------------
        stage('Checkout') {
            steps {
                echo "=========================================="
                echo "Stage 1: Checkout Source Code from GitHub"
                echo "=========================================="
                checkout scm
                script {
                    def commitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    def commitAuthor = sh(script: 'git log -1 --pretty=format:"%an <%ae>"', returnStdout: true).trim()
                    def commitMessage = sh(script: 'git log -1 --pretty=format:"%s"', returnStdout: true).trim()
                    echo "Checked out commit: ${commitHash}"
                    echo "Commit Author:     ${commitAuthor}"
                    echo "Commit Subject:    ${commitMessage}"
                }
            }
        }

        // ----------------------------------------------------
        // Stage 2: Compile and Package (Maven Build)
        // ----------------------------------------------------
        stage('Build') {
            steps {
                echo "=========================================="
                echo "Stage 2: Compile & Package Application"
                echo "=========================================="
                // Compile & package executable fat-JAR skipping tests (run in dedicated stage)
                sh 'mvn clean package -DskipTests -B'
                
                // Archive the generated executable JAR as a build artifact
                archiveArtifacts artifacts: 'target/*.jar', fingerprint: true, allowEmptyArchive: false
            }
        }

        // ----------------------------------------------------
        // Stage 3: Automated Testing & JUnit Reporting
        // ----------------------------------------------------
        stage('Test') {
            steps {
                echo "=========================================="
                echo "Stage 3: Run Unit & Integration Tests"
                echo "=========================================="
                // Execute JUnit 5 unit tests and MockMvc integration tests
                sh 'mvn test -B'
            }
            post {
                always {
                    echo "Publishing JUnit test results from target/surefire-reports/..."
                    // Collect and publish JUnit XML test reports for Jenkins dashboard
                    junit testResults: 'target/surefire-reports/*.xml',
                          allowEmptyResults: false,
                          keepLongStdio: true
                }
                failure {
                    echo "WARNING: Test phase failed! Build will terminate before Docker build."
                }
            }
        }

        // ----------------------------------------------------
        // Stage 4: Docker Multi-Stage Image Build
        // ----------------------------------------------------
        stage('Docker Build') {
            steps {
                echo "=========================================="
                echo "Stage 4: Build Multi-Stage Docker Image"
                echo "=========================================="
                script {
                    echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} and ${DOCKER_IMAGE_NAME}:latest"
                    sh """
                        docker build \
                            --build-arg BUILD_NUMBER=${DOCKER_TAG} \
                            -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} \
                            -t ${DOCKER_IMAGE_NAME}:latest \
                            .
                    """
                    echo "Docker image built successfully:"
                    sh "docker images | grep ${APP_NAME} || true"
                }
            }
        }

        // ----------------------------------------------------
        // Stage 5: Push Image to Docker Hub
        // ----------------------------------------------------
        stage('Push') {
            steps {
                echo "=========================================="
                echo "Stage 5: Push Image to Docker Hub Registry"
                echo "=========================================="
                // Use Jenkins Credentials Store to avoid exposing passwords in logs
                withCredentials([usernamePassword(
                    credentialsId: env.DOCKERHUB_CREDENTIALS_ID,
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASSWORD'
                )]) {
                    script {
                        echo "Authenticating with Docker Hub as ${DOCKERHUB_USER}..."
                        sh 'echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USER" --password-stdin'
                        
                        echo "Pushing ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}..."
                        sh "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                        
                        echo "Pushing ${DOCKER_IMAGE_NAME}:latest..."
                        sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                        
                        echo "Cleaning up local Docker Hub authentication session..."
                        sh 'docker logout'
                    }
                }
            }
        }

        // ----------------------------------------------------
        // Stage 6: Orchestrated Deployment & Health Verification
        // ----------------------------------------------------
        stage('Deploy') {
            steps {
                echo "=========================================="
                echo "Stage 6: Deploy Stack with Docker Compose"
                echo "=========================================="
                script {
                    echo "Deploying/updating multi-container stack (API + Nginx reverse proxy)..."
                    // Pull updated latest image or recreate containers idempotently
                    sh """
                        docker compose down --remove-orphans || true
                        docker compose up -d --force-recreate
                    """
                    
                    echo "Verifying running containers..."
                    sh "docker compose ps"
                    
                    echo "Awaiting service readiness and verifying Actuator health probe..."
                    sh '''
                        MAX_RETRIES=20
                        RETRY_COUNT=1
                        SUCCESS=0

                        echo "Polling ${HEALTHCHECK_URL} for healthy status..."
                        until [ $RETRY_COUNT -gt $MAX_RETRIES ]; do
                            HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${HEALTHCHECK_URL}" || true)
                            if [ "$HTTP_STATUS" = "200" ]; then
                                HEALTH_BODY=$(curl -s "${HEALTHCHECK_URL}" || true)
                                echo "Healthcheck succeeded on attempt ${RETRY_COUNT}: ${HEALTH_BODY}"
                                SUCCESS=1
                                break
                            fi
                            echo "Attempt ${RETRY_COUNT}/${MAX_RETRIES}: Received HTTP ${HTTP_STATUS}, retrying in 3s..."
                            sleep 3
                            RETRY_COUNT=$((RETRY_COUNT + 1))
                        done

                        if [ $SUCCESS -ne 1 ]; then
                            echo "ERROR: Deployment health verification failed after ${MAX_RETRIES} attempts!"
                            echo "Diagnostic logs for calculator-api:"
                            docker compose logs --tail=50 calculator-api
                            echo "Diagnostic logs for nginx:"
                            docker compose logs --tail=50 nginx
                            exit 1
                        fi
                    '''

                    echo "Performing automated smoke test through Nginx reverse proxy..."
                    sh '''
                        CALC_RESPONSE=$(curl -s "${SMOKE_TEST_URL}" || true)
                        echo "Smoke test response from ${SMOKE_TEST_URL}:"
                        echo "${CALC_RESPONSE}"
                        
                        if echo "${CALC_RESPONSE}" | grep -q '"result":30'; then
                            echo "SUCCESS: Calculator API responded correctly through Nginx reverse proxy!"
                        else
                            echo "ERROR: Smoke test assertion failed! Expected result 30."
                            exit 1
                        fi
                    '''
                }
            }
        }
    }

    // ----------------------------------------------------
    // Post-Execution Handling & Notifications
    // ----------------------------------------------------
    post {
        success {
            echo "=========================================================="
            echo "🎉 PIPELINE SUCCESSFUL: Build #${env.BUILD_NUMBER} Deployed Cleanly!"
            echo "=========================================================="
            script {
                def emailSubject = "SUCCESS: Jenkins Build #${env.BUILD_NUMBER} - Calculator REST API"
                def emailBody = """
Hi Harsh,

Great news! The Jenkins CI/CD pipeline for the Calculator REST API completed successfully.

Build Details:
--------------------------------------------------
Project:         Calculator REST API (SPE Mini-Project)
Build Number:    #${env.BUILD_NUMBER}
Build URL:       ${env.BUILD_URL}
Docker Image:    ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_TAG}
Docker Hub URL:  https://hub.docker.com/r/${env.DOCKER_IMAGE_NAME}
Deployment:      Active & Healthy via Nginx Reverse Proxy (Port 80)
Health Endpoint: ${env.HEALTHCHECK_URL}

Pipeline Stages Executed:
[✓] 1. Checkout (Git / GitHub)
[✓] 2. Build (Maven package)
[✓] 3. Test (JUnit 5 + MockMvc - Reports Published)
[✓] 4. Docker Build (Multi-stage Alpine JRE)
[✓] 5. Push (Docker Hub registry authenticated)
[✓] 6. Deploy (Docker Compose + Actuator Health Verified)

Status: DEPLOYMENT READY FOR LIVE DEMO
--------------------------------------------------
Regards,
Jenkins CI/CD Automation Agent
"""
                try {
                    mail to: env.NOTIFICATION_EMAIL,
                         subject: emailSubject,
                         body: emailBody
                    echo "Notification email dispatched to ${env.NOTIFICATION_EMAIL}"
                } catch (Exception e) {
                    echo "Email notification skipped or SMTP not configured in Jenkins: ${e.message}"
                    echo "Formatted Email Preview:\n${emailBody}"
                }
            }
        }

        failure {
            echo "=========================================================="
            echo "❌ PIPELINE FAILED: Build #${env.BUILD_NUMBER} Encountered Errors"
            echo "=========================================================="
            script {
                def emailSubject = "FAILED: Jenkins Build #${env.BUILD_NUMBER} - Calculator REST API"
                def emailBody = """
ALERT: Jenkins CI/CD pipeline build #${env.BUILD_NUMBER} failed!

Please inspect the build logs for troubleshooting:
Build URL: ${env.BUILD_URL}console

Troubleshooting Checklist:
- Check test results in target/surefire-reports/
- Verify Docker Hub credentials '${env.DOCKERHUB_CREDENTIALS_ID}'
- Check Docker daemon status and disk capacity
"""
                try {
                    mail to: env.NOTIFICATION_EMAIL,
                         subject: emailSubject,
                         body: emailBody
                } catch (Exception e) {
                    echo "Email notification skipped or SMTP not configured: ${e.message}"
                }
            }
        }

        always {
            script {
                echo "Pipeline execution finished. Cleaning up dangling Docker build cache..."
                sh 'docker image prune -f || true'
            }
        }
    }
}
