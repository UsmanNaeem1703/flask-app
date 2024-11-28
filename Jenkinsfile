flag = false
pipeline {
    agent any
    environment {
        NEW_VERSION = '1.3.0'
    }
    stages {
        stage('Setup') {
            steps {
                echo 'Setting up environment...'
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate'
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Build') {
            steps {
                echo 'Building...'
                bat 'start /B python app.py'
            }
        }
        stage('Test') {
            steps {
                script {
                    if (flag == false) {
                        echo 'Testing...'
                        // Adjust the testing command according to your setup
                        bat 'pytest'
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                bat 'taskkill /IM python.exe /F'
                bat 'start /B python app.py'
            }
        }
    }
}

