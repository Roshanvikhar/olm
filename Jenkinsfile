pipeline {
    environment {
        dockerImage = "449166544600.dkr.ecr.us-east-1.amazonaws.com/demo-app"
        workdir = "demo-app/"
        imageTag = sh(script: "date +%y%m%d%H%M%S", returnStdout: true).trim()
    }
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  serviceAccountName: jenkins-admin
                  accessModes:
                  - ReadWriteMany
                  volumes:
                  - name: docker-socket
                    emptyDir: {}
                  containers:
                  - name: docker
                    image: public.ecr.aws/p1h2b7r2/jenkins-slave
                    command:
                    - sleep
                    args:
                    - 99d
                    volumeMounts:
                    - name: docker-socket
                      mountPath: /var/run
                  - name: docker-daemon
                    image: docker:19.03.1-dind
                    securityContext:
                      privileged: true
                    volumeMounts:
                    - name: docker-socket
                      mountPath: /var/run
            '''
        }
    }
    parameters {
        string(defaultValue: 'AKIAWRFDJR3MNY5Z347U', description: 'AWS Access Key ID', name: 'AWS_ACCESS_KEY_ID')
        string(defaultValue: 'NcfpQn59+vzLVV1ujhHQvxw51UFIUfZM2maVmMJ5', description: 'AWS Secret Access Key', name: 'AWS_SECRET_ACCESS_KEY')
    }
    stages {
        stage('Git Checkout') {
            steps {
                container('docker') {
                    git branch: 'develop', credentialsId: 'jenkins-token', url: 'https://github.com/Roshanvikhar/olm.git'
                }
            }
        }

        stage('Credentials Setup') {
            steps {
                container("docker") {
                    // Get the ECR login password
                    sh ecrLoginPassword = sh(script: "aws ecr get-login-password --region ap-south-1", returnStdout: true).trim()
                    // Use the password as input to docker login
                    sh "echo ${ecrLoginPassword} | docker login --username AWS --password-stdin 449166544600.dkr.ecr.ap-south-1.amazonaws.com"
                    // The rest of the pipeline steps
                    sh "docker build -t $dockerImage:$imageTag $workdir"
                }
            }
        }
        stage('Build Prayer') {
                steps {
                container('docker') {
                   sh 'ls -l && pwd'
                   echo "Docker image and tag :: ${dockerImage}:${imageTag}"
                   sh 'cd ${workdir}; pwd; docker version && DOCKER_BUILDKIT=1 docker build -f Dockerfile -t ${dockerImage}:${imageTag} .'
        }
    }
}

        stage('Push') {
    steps {
        container('docker') {
            // Set environment variables for AWS access key ID and secret access key
            // Log in to ECR using environment variables
            sh "docker login -u AWS -p \"$AWS_SECRET_ACCESS_KEY\" 449166544600.dkr.ecr.ap-south-1.amazonaws.com"
            // Push the Docker image to ECR
            sh "docker push ${dockerImage}:${imageTag}"
                }
            }
        }

        stage('Deploy') {
            steps {
                container('docker') {
                    sh "sed -i -e 's#dockerImage#${dockerImage}#' ${workdir}/deployment/deployment.yaml" 
                    sh "sed -i -e 's#imageTag#${imageTag}#' ${workdir}/deployment/deployment.yaml"
                    sh "kubectl apply -k ${workdir}/deployment"
                }
            }
        }
    }
}
