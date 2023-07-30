pipeline {
    environment {
        dockerImage = "449166544600.dkr.ecr.us-east-1.amazonaws.com/demo-app"
        workdir = "demo-app/"
        imageTag = sh(script: "date +%y%m%d%H%M%S", returnStdout: true).trim()
        AWS_ACCESS_KEY_ID = credentials('awscredentials').AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY = credentials('awscredentials').AWS_SECRET_ACCESS_KEY
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
                script {
                    sh 'mkdir -p ~/.aws'
                    sh 'echo "[default]" > ~/.aws/credentials'
                    sh "echo 'aws_access_key_id = ${env.AWS_ACCESS_KEY_ID}' >> ~/.aws/credentials"
                    sh "echo 'aws_secret_access_key = ${env.AWS_SECRET_ACCESS_KEY}' >> ~/.aws/credentials"
          }
        }
      }
    }
     stage('Docker Login') {
            steps {
                script {
                  sh "aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 449166544600.dkr.ecr.ap-south-1.amazonaws.com"
                }
            }
        }
     stage('Kube Config') {
        steps {
            container('docker') {
          withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
            sh(script: 'mkdir -p /root/.kube')
            sh(script: "cp $KUBECONFIG /root/.kube")
          }
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
       stage('Push Prayer') {
      steps {
        container('docker') {
          sh 'docker push ${dockerImage}:${imageTag}'
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

