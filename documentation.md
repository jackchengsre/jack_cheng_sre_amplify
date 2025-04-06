# SRE Copilot Enhanced Solution Documentation

## Overview

The SRE Copilot is an AI-powered solution for root cause analysis and incident management, designed to help Site Reliability Engineers (SREs) quickly identify and resolve issues in cloud environments. This enhanced version includes a modern React.js frontend deployed to AWS Amplify and a FastAPI backend deployed to AWS Elastic Beanstalk, providing a complete end-to-end solution.

## Architecture

The SRE Copilot follows a modern microservices architecture with the following components:

### Frontend (React.js + AWS Amplify)
- **React.js**: Modern UI framework with TypeScript for type safety
- **Redux Toolkit**: State management
- **Material-UI**: Component library for consistent design
- **Axios**: API client for backend communication
- **Chart.js**: Data visualization
- **AWS Amplify**: Hosting and continuous deployment

### Backend (FastAPI + AWS Elastic Beanstalk)
- **FastAPI**: Modern, high-performance Python web framework
- **Pydantic**: Data validation and settings management
- **SQLAlchemy**: ORM for database interactions
- **AWS SDK (Boto3)**: AWS service integrations
- **AWS Bedrock**: AI model inference for analysis
- **Docker**: Containerization
- **AWS Elastic Beanstalk**: Hosting and deployment

### AWS Integration
- **AWS Bedrock**: Foundation models for AI-powered analysis
  - Claude 3 Haiku: Log analysis
  - Amazon Titan Text: Metrics analysis
  - Amazon Nova Lite: Dashboard analysis
  - Amazon Titan Embeddings: Knowledge base
  - Amazon Nova Pro: Supervisor agent
- **CloudWatch**: Logs and metrics
- **S3**: Storage for analysis artifacts
- **DynamoDB**: Knowledge base storage

## Features

### Incident Management
- Create, view, update, and delete incidents
- Track incident status, severity, and affected services
- View incident history and timeline

### Multi-Modal Analysis
- Analyze incidents using logs, metrics, and dashboard data
- AI-powered root cause identification
- Correlation of events across different data sources
- Recommendations for resolution

### Knowledge Base
- Store and retrieve past incidents and resolutions
- Semantic search for similar incidents
- Tag-based organization
- AI-powered recommendations based on past incidents

### Dashboard
- Real-time system status monitoring
- Visualization of key metrics
- Incident trends and statistics

## Deployment

### Frontend Deployment (AWS Amplify)

1. **Prerequisites**:
   - AWS account with Amplify access
   - GitHub repository with the frontend code

2. **Steps**:
   - Connect your GitHub repository to AWS Amplify
   - Configure build settings using the provided `amplify.yml`
   - Set environment variables:
     - `REACT_APP_API_BASE_URL`: URL of your backend API
   - Deploy the application

3. **Configuration**:
   The `amplify.yml` file in the frontend directory configures the build process:
   ```yaml
   version: 1
   frontend:
     phases:
       preBuild:
         commands:
           - npm ci
       build:
         commands:
           - echo "REACT_APP_API_BASE_URL=$API_BASE_URL" >> .env
           - npm run build
     artifacts:
       baseDirectory: build
       files:
         - '**/*'
     cache:
       paths:
         - node_modules/**/*
         - .npm/**/*
   ```

### Backend Deployment (AWS Elastic Beanstalk)

1. **Prerequisites**:
   - AWS account with Elastic Beanstalk access
   - Docker installed locally for testing

2. **Steps**:
   - Create a new Elastic Beanstalk environment
   - Choose Docker as the platform
   - Upload the backend code as a ZIP file
   - Configure environment variables:
     - `ENVIRONMENT`: `production`
     - `LOG_LEVEL`: `INFO`
     - `AWS_REGION`: Your AWS region
     - `AWS_ACCESS_KEY_ID`: Your AWS access key
     - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - Deploy the application

3. **Configuration**:
   The backend includes several configuration files:
   - `Dockerfile`: Defines the container environment
   - `requirements.txt`: Lists Python dependencies
   - `.ebextensions/01_fastapi.config`: Configures the Elastic Beanstalk environment

## Development Setup

### Frontend Development

1. **Prerequisites**:
   - Node.js 16+
   - npm or yarn

2. **Setup**:
   ```bash
   cd frontend
   npm install
   ```

3. **Environment Configuration**:
   Create a `.env` file in the frontend directory:
   ```
   REACT_APP_API_BASE_URL=http://localhost:8000
   ```

4. **Run Development Server**:
   ```bash
   npm start
   ```

5. **Build for Production**:
   ```bash
   npm run build
   ```

### Backend Development

1. **Prerequisites**:
   - Python 3.10+
   - pip

2. **Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   Create a `.env` file in the backend directory:
   ```
   ENVIRONMENT=development
   LOG_LEVEL=DEBUG
   ```

4. **Run Development Server**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Run Tests**:
   ```bash
   pytest
   ```

## API Reference

### Incidents API

- `GET /api/v1/incidents`: List all incidents
- `GET /api/v1/incidents/{id}`: Get incident details
- `POST /api/v1/incidents`: Create a new incident
- `PUT /api/v1/incidents/{id}`: Update an incident
- `DELETE /api/v1/incidents/{id}`: Delete an incident

### Analysis API

- `GET /api/v1/analysis`: List all analyses
- `GET /api/v1/analysis/{id}`: Get analysis details
- `POST /api/v1/analysis`: Create a new analysis
- `POST /api/v1/bedrock/analyze`: Perform AI-powered analysis

### Knowledge Base API

- `GET /api/v1/knowledge`: Search knowledge base
- `GET /api/v1/knowledge/{id}`: Get knowledge base entry
- `POST /api/v1/knowledge`: Create a new knowledge base entry
- `PUT /api/v1/knowledge/{id}`: Update a knowledge base entry
- `DELETE /api/v1/knowledge/{id}`: Delete a knowledge base entry

### CloudWatch API

- `POST /api/v1/aws/cloudwatch/metrics`: Get CloudWatch metrics

## AWS Bedrock Integration

The SRE Copilot uses AWS Bedrock foundation models for AI-powered analysis:

1. **Log Analysis Agent (Claude 3 Haiku)**
   - Analyzes log data to identify patterns and anomalies
   - Extracts relevant events and errors
   - Correlates log entries with incident timeline

2. **Metrics Analysis Agent (Amazon Titan Text)**
   - Analyzes time-series metrics data
   - Identifies anomalies and trends
   - Correlates metrics with incident timeline

3. **Dashboard Analysis Agent (Amazon Nova Lite)**
   - Interprets dashboard visualizations
   - Extracts insights from charts and graphs
   - Identifies visual patterns in monitoring data

4. **Knowledge Base Agent (Amazon Titan Embeddings)**
   - Generates embeddings for knowledge base entries
   - Performs semantic search on knowledge base
   - Finds similar past incidents

5. **Supervisor Agent (Amazon Nova Pro)**
   - Coordinates the specialized agents
   - Synthesizes findings from different data sources
   - Generates comprehensive root cause analysis

## Testing

The solution includes comprehensive testing:

1. **Unit Tests**:
   - Frontend: Jest and React Testing Library
   - Backend: pytest

2. **End-to-End Tests**:
   - `test_end_to_end.py`: Tests the complete solution
   - Tests all API endpoints
   - Verifies deployment configurations

## Security Considerations

1. **Authentication and Authorization**:
   - JWT-based authentication
   - Role-based access control
   - Secure credential storage

2. **Data Protection**:
   - HTTPS for all communications
   - Encryption for sensitive data
   - Proper handling of AWS credentials

3. **Infrastructure Security**:
   - Least privilege principle for IAM roles
   - Network security with proper VPC configuration
   - Regular security updates

## Performance Considerations

1. **Scalability**:
   - Auto-scaling for both frontend and backend
   - Database connection pooling
   - Asynchronous processing for long-running analyses

2. **Caching**:
   - Frontend caching for static assets
   - API response caching
   - Database query optimization

## Troubleshooting

### Common Issues

1. **Frontend Issues**:
   - Check browser console for errors
   - Verify API base URL configuration
   - Check network requests for API communication

2. **Backend Issues**:
   - Check application logs
   - Verify AWS credentials and permissions
   - Check database connectivity

3. **Deployment Issues**:
   - Review deployment logs in AWS console
   - Verify configuration files
   - Check environment variables

### Logging

- Frontend: Console logging and error tracking
- Backend: Structured logging with correlation IDs
- AWS: CloudWatch Logs for all components

## Next Steps

1. **Production Readiness**:
   - Implement CI/CD pipelines
   - Set up monitoring and alerting
   - Perform security audit

2. **Feature Enhancements**:
   - Real-time notifications
   - Advanced visualization
   - Integration with additional AWS services

3. **AI Improvements**:
   - Fine-tuning foundation models
   - Expanding knowledge base
   - Implementing feedback loops for continuous improvement

## Conclusion

The enhanced SRE Copilot provides a powerful solution for incident management and root cause analysis, leveraging modern web technologies and AWS services. The combination of a React.js frontend and FastAPI backend, along with AWS Bedrock foundation models, creates a comprehensive tool for SREs to quickly identify and resolve issues in cloud environments.
