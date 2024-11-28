flag = true
pipeline {
    agent any
    environment {
        NEW_VERSION = '1.3.0'
    }
    stages {
        stage('Setup') {
            steps {
                echo 'Setting up environment...'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'python app.py &'
            }
        }
        stage('Test') {
            steps {
                script {
                    if (flag == false) {
                        echo 'Testing...'
                        // Add your testing commands, e.g., pytest or other test runner
                        sh 'pytest'
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                // Assuming deployment to a local or remote server, use appropriate commands
                sh 'pkill python' // Optionally stop the current running app
                sh 'nohup python app.py &'
            }
        }
    }
}
