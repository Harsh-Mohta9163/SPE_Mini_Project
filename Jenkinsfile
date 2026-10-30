pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    triggers {
        githubPush()
        pollSCM('H/5 * * * *')
    }

    environment {
        IMAGE = 'harshmohta9163/calculator-api'
        CRED_ID = 'dockerhub-creds'
        NOTIFY_EMAIL = 'harshmohta9163@gmail.com'
        // Add Windows tools to PATH for local Jenkins service
        PATH = "C:\\Program Files\\Git\\bin;C:\\Program Files\\Git\\cmd;C:\\Users\\dell\\maven\\bin;C:\\Users\\dell\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;C:\\Users\\dell\\AppData\\Local\\Programs\\Python\\Python312;${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'mvn clean package -DskipTests -B'
                    } else {
                        bat 'mvn clean package -DskipTests -B'
                    }
                }
                archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
            }
        }

        stage('Test') {
            steps {
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
                    junit testResults: 'target/surefire-reports/*.xml', allowEmptyResults: false
                }
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    def buildCmd = "docker build -t ${IMAGE}:${BUILD_NUMBER} -t ${IMAGE}:latest ."
                    if (isUnix()) {
                        sh buildCmd
                    } else {
                        bat buildCmd
                    }
                }
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: env.CRED_ID,
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    script {
                        if (isUnix()) {
                            sh 'echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin'
                            sh "docker push ${IMAGE}:${BUILD_NUMBER}"
                            sh "docker push ${IMAGE}:latest"
                            sh 'docker logout'
                        } else {
                            bat 'docker login -u "%DH_USER%" -p "%DH_PASS%"'
                            bat "docker push ${IMAGE}:${BUILD_NUMBER}"
                            bat "docker push ${IMAGE}:latest"
                            bat 'docker logout'
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker compose down --remove-orphans || true'
                        sh 'docker compose up -d --force-recreate'
                        sh 'python3 scripts/smoke_test.py || python scripts/smoke_test.py'
                    } else {
                        bat 'docker compose down --remove-orphans || exit /b 0'
                        bat 'docker compose up -d --force-recreate'
                        bat 'python scripts/smoke_test.py'
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                try {
                    mail to: env.NOTIFY_EMAIL,
                         subject: "Build #${BUILD_NUMBER} Succeeded - Calculator API",
                         body: "Pipeline build #${BUILD_NUMBER} completed successfully.\nImage: ${IMAGE}:${BUILD_NUMBER}\nConsole: ${BUILD_URL}"
                } catch (Exception e) {
                    echo "Email skipped: ${e.message}"
                }
            }
        }
        failure {
            script {
                try {
                    mail to: env.NOTIFY_EMAIL,
                         subject: "Build #${BUILD_NUMBER} Failed - Calculator API",
                         body: "Pipeline build #${BUILD_NUMBER} failed. Check console: ${BUILD_URL}"
                } catch (Exception e) {
                    echo "Email skipped: ${e.message}"
                }
            }
        }
        always {
            script {
                if (isUnix()) {
                    sh 'docker image prune -f || true'
                } else {
                    bat 'docker image prune -f || exit /b 0'
                }
            }
        }
    }
}
