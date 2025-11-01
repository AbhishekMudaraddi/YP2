// pipeline {
//     agent any
    
//     environment {
//         AWS_CREDENTIALS = credentials('aws-access-key-id') 
//         ECR_REGISTRY = "your-aws-account-id.dkr.ecr.us-east-1.amazonaws.com"
//         ECR_REPOSITORY = "ypass-app"
//         EC2_IP = "your-ec2-public-ip"
//     }
    
//     stages {
//         stage('Checkout') {
//             steps {
//                 git branch: 'main', url: 'https://github.com/AbhishekMudaraddi/YP2.git'
//             }
//         }
//     }
//       stages {
//         stage('Build Docker Image') {
//             steps {
//                 withEnv(["PATH+EXTRA=/usr/local/bin"]) {
//                     sh 'docker --version'
//                     sh 'docker build -t ypass-app .'
//                 }
//             }
//         }
//     }
        
//         stage('Push to ECR') {
//             steps {
//                 script {
//                     docker.withRegistry("https://${ECR_REGISTRY}", "ecr:us-east-1:aws-credentials") {
//                         dockerImage.push("${env.BUILD_ID}")
//                         dockerImage.push("latest")
//                     }
//                 }
//             }
//         }
        
//         stage('Deploy to EC2') {
//             steps {
//                 sshagent(['ec2-ssh-key']) {
//                     sh """
//                         ssh -o StrictHostKeyChecking=no ec2-user@${EC2_IP} \
//                         'docker stop ypass-app || true && \
//                          docker rm ypass-app || true && \
//                          docker run -d --name ypass-app \
//                          -p 5000:5000 \
//                          -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
//                          -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
//                          ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest'
//                     """
//                 }
//             }
//         }
//     }
// }




pipeline {
    agent any

    environment {
        AWS_CREDENTIALS = credentials('aws-access-key-id') 
        ECR_REGISTRY = "your-aws-account-id.dkr.ecr.us-east-1.amazonaws.com"
        ECR_REPOSITORY = "ypass-app"
        EC2_IP = "your-ec2-public-ip"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AbhishekMudaraddi/YP2.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                withEnv(["PATH+EXTRA=/usr/local/bin:/usr/bin:/bin"]) {
                    sh 'docker --version'
                    sh 'docker build -t ypass-app .'
                }
                script {
                    dockerImage = docker.build("${ECR_REPOSITORY}:${env.BUILD_ID}")
                }
            }
        }
        
        stage('Push to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        docker.withRegistry("https://${ECR_REGISTRY}", "") {
                            dockerImage.push("${env.BUILD_ID}")
                            dockerImage.push("latest")
                        }
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ec2-user@${EC2_IP} \
                        'docker stop ypass-app || true && \
                         docker rm ypass-app || true && \
                         docker run -d --name ypass-app \
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