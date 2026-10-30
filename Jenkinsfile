pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    triggers {
        githubPush()
    }

    environment {
        IMAGE = 'harsh9163/calculator-api'
        NOTIFY_EMAIL = 'harshmohta9163@gmail.com'
        // Jenkins runs as a Windows service: expose Git Bash (sh), Maven, Docker and Python to it.
        PATH = "C:\\Program Files\\Git\\bin;C:\\Program Files\\Git\\usr\\bin;C:\\Program Files\\Git\\cmd;C:\\Users\\dell\\maven\\bin;C:\\Users\\dell\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;C:\\Users\\dell\\AppData\\Local\\Programs\\Python\\Python312;${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests -B'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test -B'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE:$BUILD_NUMBER -t $IMAGE:latest .'
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'DH_USER',
                                                  passwordVariable: 'DH_PASS')]) {
                    sh 'echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin'
                    sh 'docker push $IMAGE:$BUILD_NUMBER'
                    sh 'docker push $IMAGE:latest'
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose up -d --force-recreate'
                sh 'python scripts/smoke_test.py'
            }
        }
    }

    post {
        success {
            mail to: env.NOTIFY_EMAIL,
                 subject: "Build #${BUILD_NUMBER} SUCCESS - Calculator API",
                 body: "Build #${BUILD_NUMBER} succeeded.\nImage: ${IMAGE}:${BUILD_NUMBER}\nConsole: ${BUILD_URL}"
        }
        failure {
            mail to: env.NOTIFY_EMAIL,
                 subject: "Build #${BUILD_NUMBER} FAILED - Calculator API",
                 body: "Build #${BUILD_NUMBER} failed.\nConsole: ${BUILD_URL}"
        }
        always {
            sh 'docker logout || true'
        }
    }
}
