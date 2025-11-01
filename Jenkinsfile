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
        ECR_REGISTRY = "503561414328.dkr.ecr.us-east-1.amazonaws.com"
        ECR_REPOSITORY = "ypass-app"
        EC2_IP = "ec2-54-159-40-115.compute-1.amazonaws.com"
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
                    script {
                        docker.build("${ECR_REPOSITORY}:${env.BUILD_ID}")
                    }
                }
            }
        }

        stage('Push to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-access-key-id',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    withEnv(["PATH+EXTRA=/usr/local/bin:/usr/bin:/bin"]) {
                        sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                        sh "docker tag ${ECR_REPOSITORY}:${env.BUILD_ID} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${env.BUILD_ID}"
                        sh "docker tag ${ECR_REPOSITORY}:${env.BUILD_ID} ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest"
                        sh "docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${env.BUILD_ID}"
                        sh "docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest"
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ec2-user@${EC2_IP} '
                        export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                        export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                        aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        docker stop ypass-app || true
                        docker rm ypass-app || true
                        docker run -d --name ypass-app -p 5000:5000 ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                        '
                    """
                }
            }
        }
    }
}