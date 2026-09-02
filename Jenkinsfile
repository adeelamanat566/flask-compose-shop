
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

