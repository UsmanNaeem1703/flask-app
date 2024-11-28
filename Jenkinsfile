flag = true

pipeline {
agent any
  environment {
    NEW_VERSION = '1.3.0'
  }
stages {
stage('Build') {
steps {
echo 'Building..'
// Here you can define commands for your build
}
}
stage('Test') {
steps {
  when {
    expression {
      flag == false
    }
  }
echo 'Testing..'
// Here you can define commands for your tests
}
}
stage('Deploy') {
steps {
echo 'Deploying....'
// Here you can define commands for your deployment
}
}

}
}
