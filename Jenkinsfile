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

        // Prepend Windows tools to PATH so Jenkins Windows service can locate git, sh, mvn, docker, python
        PATH = "C:\\Program Files\\Git\\bin;C:\\Program Files\\Git\\usr\\bin;C:\\Program Files\\Git\\cmd;C:\\Users\\dell\\maven\\bin;C:\\Users\\dell\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;C:\\Users\\dell\\AppData\\Local\\Programs\\Python\\Python312;C:\\Users\\dell\\AppData\\Local\\Programs\\Python\\Python312\\Scripts;${env.PATH}"
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
                    def commitHash = ""
                    def commitAuthor = ""
                    def commitMessage = ""
                    if (isUnix()) {
                        commitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                        commitAuthor = sh(script: 'git log -1 --pretty=format:"%an <%ae>"', returnStdout: true).trim()
                        commitMessage = sh(script: 'git log -1 --pretty=format:"%s"', returnStdout: true).trim()
                    } else {
                        commitHash = bat(script: '@git rev-parse --short HEAD', returnStdout: true).trim()
                        commitAuthor = bat(script: '@git log -1 --pretty=format:"%%an <%%ae>"', returnStdout: true).trim()
                        commitMessage = bat(script: '@git log -1 --pretty=format:"%%s"', returnStdout: true).trim()
                    }
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
                script {
                    if (isUnix()) {
                        sh 'mvn clean package -DskipTests -B'
                    } else {
                        bat 'mvn clean package -DskipTests -B'
                    }
                }
                
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
                script {
                    if (isUnix()) {
                        sh 'mvn test -B'
                    } else {
                        bat 'mvn test -B'
                    }
                }
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
                    if (isUnix()) {
                        sh """
                            docker build \
                                --build-arg BUILD_NUMBER=${DOCKER_TAG} \
                                -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} \
                                -t ${DOCKER_IMAGE_NAME}:latest \
                                .
                        """
                        sh "docker images | grep ${APP_NAME} || true"
                    } else {
                        bat """
                            docker build --build-arg BUILD_NUMBER=${DOCKER_TAG} -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} -t ${DOCKER_IMAGE_NAME}:latest .
                        """
                        bat "docker images | findstr ${APP_NAME} || exit /b 0"
                    }
                    echo "Docker image built successfully."
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
                        if (isUnix()) {
                            sh 'echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USER" --password-stdin'
                            echo "Pushing ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}..."
                            sh "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                            echo "Pushing ${DOCKER_IMAGE_NAME}:latest..."
                            sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                            sh 'docker logout'
                        } else {
                            bat 'echo %DOCKERHUB_PASSWORD% | docker login -u "%DOCKERHUB_USER%" --password-stdin'
                            echo "Pushing ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}..."
                            bat "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                            echo "Pushing ${DOCKER_IMAGE_NAME}:latest..."
                            bat "docker push ${DOCKER_IMAGE_NAME}:latest"
                            bat 'docker logout'
                        }
                        echo "Docker Hub publication completed successfully."
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
                    if (isUnix()) {
                        sh 'docker compose down --remove-orphans || true'
                        sh 'docker compose up -d --force-recreate'
                        sh 'docker compose ps'
                        
                        echo "Verifying deployment health via automated smoke test suite..."
                        sh 'python3 scripts/smoke_test.py || python scripts/smoke_test.py'
                    } else {
                        bat 'docker compose down --remove-orphans || exit /b 0'
                        bat 'docker compose up -d --force-recreate'
                        bat 'docker compose ps'
                        
                        echo "Verifying deployment health via automated smoke test suite..."
                        bat 'python scripts/smoke_test.py'
                    }
                    echo "Deployment verified healthy and fully functional."
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
                if (isUnix()) {
                    sh 'docker image prune -f || true'
                } else {
                    bat 'docker image prune -f || exit /b 0'
                }
            }
        }
    }
}
