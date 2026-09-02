pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['staging', 'production'],
            description: 'Select deployment environment'
        )

        booleanParam(
            name: 'DEPLOY',
            defaultValue: true,
            description: 'Deploy application after build'
        )
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Files') {
            steps {
                sh '''
                echo "Checking project files..."

                ls -la

                test -f Dockerfile
                test -f compose.staging.yaml
                test -f compose.production.yaml
                test -f requirements.txt
                test -f app.py

                echo "All required files are present."
                '''
            }
        }

        stage('Validate Compose') {
            steps {
                sh '''
                    echo "Validating Docker Compose..."
                    docker compose config
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo "Building Docker images..."
                    docker compose build
                '''
            }
        }

        stage('Deploy') {
            when {
                expression {
                    return params.DEPLOY
                }
            }

            steps {
                sh '''
                    echo "Deploying to ${ENVIRONMENT}..."

                    docker compose up -d

                    echo "Running containers:"
                    docker compose ps
                '''
            }
        }

        stage('Health Check') {
            when {
                expression {
                    return params.DEPLOY
                }
            }

            steps {
                sh '''
                    echo "Waiting for application..."
                    sleep 10

                    docker compose ps

                    echo "Testing Flask application..."
                    curl -f http://localhost:5000/

                    echo "Application is healthy!"
                '''
            }
        }
    }

    post {

        success {
            echo "Pipeline completed successfully!"
            echo "Build Number: ${BUILD_NUMBER}"
            echo "Environment: ${ENVIRONMENT}"
        }

        failure {
            echo "Pipeline FAILED!"

            sh '''
                docker compose ps || true
                docker compose logs --tail=50 || true
            '''
        }

        always {
            echo "Pipeline finished."
        }
    }
}
