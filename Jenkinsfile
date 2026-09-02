pipeline {
    agent any

    stages {

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
                    echo "Validating Staging Compose..."
                    docker compose -f compose.staging.yaml config

                    echo "Validating Production Compose..."
                    docker compose -f compose.production.yaml config
                '''
            }
        }

        stage('Build Staging') {
            steps {
                sh '''
                    echo "Building Staging..."

                    docker compose -f compose.staging.yaml build
                '''
            }
        }

        stage('Deploy Staging') {
            steps {
                sh '''
                    echo "Deploying Staging..."

                    docker compose -f compose.staging.yaml up -d

                    echo "Staging containers:"
                    docker compose -f compose.staging.yaml ps
                '''
            }
        }

        stage('Test Staging') {
            steps {
                sh '''
                    echo "Waiting for Staging..."
                    sleep 10

                    echo "Testing Staging..."

                    docker compose -f compose.staging.yaml ps

                    curl -f http://localhost:5001/

                    echo "Staging is healthy!"
                '''
            }
        }

        stage('Production Approval') {
            steps {
                input(
                    message: 'Staging tests passed. Deploy to Production?',
                    ok: 'Deploy Production'
                )
            }
        }

        stage('Build Production') {
            steps {
                sh '''
                    echo "Building Production..."

                    docker compose -f compose.production.yaml build
                '''
            }
        }

        stage('Deploy Production') {
            steps {
                sh '''
                    echo "Deploying Production..."

                    docker compose -f compose.production.yaml up -d

                    echo "Production containers:"
                    docker compose -f compose.production.yaml ps
                '''
            }
        }

        stage('Test Production') {
            steps {
                sh '''
                    echo "Waiting for Production..."
                    sleep 10

                    echo "Testing Production..."

                    docker compose -f compose.production.yaml ps

                    curl -f http://localhost:5000/

                    echo "Production is healthy!"
                '''
            }
        }
    }

    post {

        success {
            echo "Pipeline completed successfully!"
        }

        failure {
            echo "Pipeline FAILED!"

            sh '''
                echo "Staging containers:"
                docker compose -f compose.staging.yaml ps || true

                echo "Staging logs:"
                docker compose -f compose.staging.yaml logs --tail=50 || true

                echo "Production containers:"
                docker compose -f compose.production.yaml ps || true

                echo "Production logs:"
                docker compose -f compose.production.yaml logs --tail=50 || true
            '''
        }

        always {
            echo "Pipeline finished."
        }
    }
}
