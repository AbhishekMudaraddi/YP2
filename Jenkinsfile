pipeline {
    agent any
    
    environment {
        AWS_CREDENTIALS = credentials('aws-access-key-id') 
        ECR_REGISTRY = "your-aws-account-id.dkr.ecr.us-east-1.amazonaws.com"
        ECR_REPOSITORY = "flask-auth-app"
        EC2_IP = "your-ec2-public-ip"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-username/flask-auth-app.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${ECR_REPOSITORY}")
                }
            }
        }
        
        stage('Push to ECR') {
            steps {
                script {
                    docker.withRegistry("https://${ECR_REGISTRY}", "ecr:us-east-1:aws-credentials") {
                        dockerImage.push("${env.BUILD_ID}")
                        dockerImage.push("latest")
                    }
                }
            }
        }
        
        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ec2-user@${EC2_IP} \
                        'docker stop flask-auth-app || true && \
                         docker rm flask-auth-app || true && \
                         docker run -d --name flask-auth-app \
                         -p 5000:5000 \
                         -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
                         -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
                         ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest'
                    """
                }
            }
        }
    }
}