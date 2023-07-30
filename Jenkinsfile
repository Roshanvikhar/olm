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
            image: 535688970980.dkr.ecr.ap-south-1.amazonaws.com/jenkins-slave:1
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
          git branch: 'develop', credentialsId: 'jenkins-token', url: ''https://github.com/Roshanvikhar/olm.git'
        }
      }
    }
  }
}