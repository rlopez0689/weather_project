pipeline {
    agent any

    stages {
        stage('Get Project') {
            steps {
                sh 'rm -rf weather_project'
                sh 'git clone git@github.com:rlopez0689/weather_project.git'
                sh "virtualenv env"
                sh ". env/bin/activate && pip install -r weather_project/requirements.txt"
            }
        }
        stage('Test') {
            steps {
                sh '. env/bin/activate && cd weather_project && python manage.py test'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
