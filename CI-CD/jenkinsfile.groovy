pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your_username/your_repository.git'
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                sh 'docker build -t your-container-registry/your-image-name:latest .'
                sh 'docker push your-container-registry/your-image-name:latest'
            }
        }

        stage('Deploy to Cloud') {
            steps {
                ansiblePlaybook(
                    playbook: '/path/to/your/ansible/playbook.yml',
                    inventory: '/path/to/your/ansible/inventory.ini',
                    extras: '-e "your_extra_variables_if_needed"'
                )
            }
        }
    }
}
