pipeline {
    agent any
    stages {
        stage('build'){
            steps { 
            sh 'docker compose build'
            }
        
        
        }
        stage('test'){
            
                steps {
                sh 'docker compose up -d '
                
                }
            
        
        
        
        }
        stage('input'){
            steps {
                input (
                    message: 'we continue'
                )
            
            }
        
        
        
        
        }
        stage('deploy'){
            steps {
                sh 'docker compose up -d' 
                
            
            }

        }
    }    
    post {
        always {
            echo "fininshed"
            }
        failure {
            echo "failure"

            }
        success {
            echo "success"
            }

        
        
        }
    
    
    
    

}
