pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = "dockerhub-creds"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_BACKEND = "yashdubey455/backend-app:${IMAGE_TAG}"
        IMAGE_FRONTEND = "yashdubey455/frontend:${IMAGE_TAG}"
    }
    
    stages {
        stage('clone repo') {
            steps{
                git branch: 'main',
                credentialsId: 'github-creds',
                url: 'https://github.com/Yashdubey455/DevOps-Application.git'
                
            }
        }
        stage('build image') {
            steps {
                sh 'docker build -t $IMAGE_BACKEND ./backend'
                sh 'docker build -t $IMAGE_FRONTEND ./frontend'
            }
        }
        stage('login to dockerhub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                    )]) {
                     sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    }
            }
        }
        stage('push dockerhub'){
            steps  {
                sh 'docker push $IMAGE_BACKEND'
                sh 'docker push $IMAGE_FRONTEND'
            }
        }
        stage('Update K8s YAML & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {

                    sh '''
                    # update image in YAML
                    sed -i "s|image:.*backend-app.*|image: yashdubey455/backend-app:${IMAGE_TAG}|g" k8s/backend-deployment.yaml
                    sed -i "s|image:.*frontend.*|image: yashdubey455/frontend:${IMAGE_TAG}|g" k8s/frontend-deployment.yaml

                    # git config
                    git config user.name "jenkins"
                    git config user.email "jenkins@local"

                    # commit changes
                    git add k8s/
                    git commit -m "Update image via Jenkins" || echo "No changes"

                    # push using credentials
                    git push https://$GIT_USER:$GIT_PASS@github.com/Yashdubey455/DevOps-Application.git main
                    '''
                }
            }
        }
    }
}
