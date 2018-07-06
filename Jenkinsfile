pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        git(url: 'https://github.com/oherrou/GitLog.git', branch: 'master')
      }
    }
    stage('Syntax Check') {
      steps {
        echo 'Syntax check'
      }
    }
    stage('Build') {
      steps {
        echo 'Building'
      }
    }
    stage('Reporting') {
      steps {
        echo 'Reporting'
      }
    }
    stage('Static analysis') {
      steps {
        echo 'Static analysis'
      }
    }
    stage('Unit test') {
      steps {
        echo 'Unit Testing'
      }
    }
    stage('Deployment') {
      steps {
        echo 'Deployment'
      }
    }
  }
}