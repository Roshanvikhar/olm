pipeline {
  environment {
    dockerImagePrayer = '449166544600.dkr.ecr.us-east-1.amazonaws.com/demo-app'
    workdir =  'demo-app/'
    def imageTag = sh(script: 'echo `date +%y%m%d%H%M%S`', returnStdout: true).trim()
  }
  agent {
    kubernetes {
      yaml '''
        apiVersion: v1
        kind: Pod
        spec:
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
          git branch: 'develop', credentialsId: 'jenkins-token', url: "https://github.com/Roshanvikhar/olm.git"
        }
      }
    }
    stage('Credentials Setup') {
      steps {
        container('docker') {
          withCredentials([file(credentialsId: 'awscredentials', variable: 'AWS_SHARED_CREDENTIALS_FILE')]) {
            sh(script: 'mkdir -p /root/.aws')
            sh(script: "cp $AWS_SHARED_CREDENTIALS_FILE /root/.aws")
            sh(script: ' aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 449166544600.dkr.ecr.ap-south-1.amazonaws.com')
          }
        }
      }
    }
  }
}