# SRE Copilot Backend Architecture

This document outlines the architecture for the FastAPI backend of the SRE Copilot application, which will be deployed to AWS Elastic Beanstalk.

## Overview

The SRE Copilot backend will provide a robust API for the React frontend to interact with AWS Bedrock foundation models for incident analysis, knowledge base management, and other SRE-related functionalities.

## Technology Stack

- **FastAPI**: Modern, high-performance web framework for building APIs
- **Python 3.10+**: For backend logic
- **Pydantic**: For data validation and settings management
- **SQLAlchemy**: For ORM and database interactions
- **AWS SDK for Python (Boto3)**: For AWS service interactions
- **AWS Bedrock**: For AI model inference
- **JWT**: For authentication and authorization
- **Pytest**: For testing
- **Docker**: For containerization
- **AWS Elastic Beanstalk**: For deployment

## API Structure

```
app/
├── main.py                  # FastAPI application entry point
├── core/                    # Core application modules
│   ├── config.py            # Application configuration
│   ├── security.py          # Authentication and authorization
│   └── logging.py           # Logging configuration
├── api/                     # API endpoints
│   ├── v1/                  # API version 1
│   │   ├── endpoints/       # API endpoint modules
│   │   │   ├── incidents.py # Incidents endpoints
│   │   │   ├── analysis.py  # Analysis endpoints
│   │   │   ├── knowledge.py # Knowledge base endpoints
│   │   │   └── metrics.py   # Metrics endpoints
│   │   └── router.py        # API router
│   └── deps.py              # Dependency injection
├── models/                  # Database models
│   ├── incident.py          # Incident model
│   ├── analysis.py          # Analysis model
│   └── knowledge.py         # Knowledge base model
├── schemas/                 # Pydantic schemas
│   ├── incident.py          # Incident schemas
│   ├── analysis.py          # Analysis schemas
│   └── knowledge.py         # Knowledge base schemas
├── services/                # Business logic services
│   ├── incident.py          # Incident service
│   ├── analysis.py          # Analysis service
│   ├── knowledge.py         # Knowledge base service
│   └── aws/                 # AWS service integrations
│       ├── bedrock.py       # AWS Bedrock integration
│       ├── cloudwatch.py    # CloudWatch integration
│       └── s3.py            # S3 integration
├── db/                      # Database
│   ├── base.py              # Base model
│   ├── session.py           # Database session
│   └── init_db.py           # Database initialization
├── utils/                   # Utility functions
│   ├── logging.py           # Logging utilities
│   └── helpers.py           # Helper functions
└── tests/                   # Tests
    ├── conftest.py          # Test configuration
    ├── api/                 # API tests
    └── services/            # Service tests
```

## Endpoints

### Incidents API

```
GET /api/v1/incidents - List incidents
GET /api/v1/incidents/{id} - Get incident details
POST /api/v1/incidents - Create incident
PUT /api/v1/incidents/{id} - Update incident
DELETE /api/v1/incidents/{id} - Delete incident
```

### Analysis API

```
POST /api/v1/analysis - Submit analysis request
GET /api/v1/analysis/{id} - Get analysis results
GET /api/v1/analysis - List analyses
```

### Knowledge Base API

```
GET /api/v1/knowledge - Search knowledge base
GET /api/v1/knowledge/{id} - Get knowledge base entry
POST /api/v1/knowledge - Create knowledge base entry
PUT /api/v1/knowledge/{id} - Update knowledge base entry
DELETE /api/v1/knowledge/{id} - Delete knowledge base entry
```

### Metrics API

```
GET /api/v1/metrics/cloudwatch - Get CloudWatch metrics
POST /api/v1/metrics/analyze - Analyze metrics
```

## Data Models

### Incident Model

```python
class Incident(Base):
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    severity = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    services = Column(ARRAY(String))
    analyses = relationship("Analysis", back_populates="incident")
```

### Analysis Model

```python
class Analysis(Base):
    id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, ForeignKey("incident.id"))
    type = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    log_data = Column(Text)
    metrics_data = Column(Text)
    dashboard_data = Column(Text)
    result = Column(JSON)
    incident = relationship("Incident", back_populates="analyses")
```

### Knowledge Base Entry Model

```python
class KnowledgeBaseEntry(Base):
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    root_cause = Column(String)
    resolution = Column(String)
    services = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = Column(ARRAY(String))
    embedding = Column(ARRAY(Float))
```

## AWS Bedrock Integration

The backend will integrate with AWS Bedrock to provide AI-powered analysis capabilities:

1. **Log Analysis Agent (Claude 3 Haiku)**
   - Analyze log data to identify patterns and anomalies
   - Extract relevant events and errors
   - Correlate log entries with incident timeline

2. **Metrics Analysis Agent (Amazon Titan Text)**
   - Analyze time-series metrics data
   - Identify anomalies and trends
   - Correlate metrics with incident timeline

3. **Dashboard Analysis Agent (Amazon Nova Lite)**
   - Interpret dashboard visualizations
   - Extract insights from charts and graphs
   - Identify visual patterns in monitoring data

4. **Knowledge Base Agent (Amazon Titan Embeddings)**
   - Generate embeddings for knowledge base entries
   - Perform semantic search on knowledge base
   - Find similar past incidents

5. **Supervisor Agent (Amazon Nova Pro)**
   - Coordinate the specialized agents
   - Synthesize findings from different data sources
   - Generate comprehensive root cause analysis

## Authentication and Authorization

The backend will use JWT-based authentication with the following features:

1. **User Authentication**
   - Login with username/password
   - JWT token generation and validation
   - Token refresh

2. **Role-Based Access Control**
   - Admin role: Full access
   - Analyst role: Read/write access to incidents and analyses
   - Viewer role: Read-only access

## AWS Integration

The backend will integrate with various AWS services:

1. **AWS Bedrock**
   - Model inference for AI-powered analysis
   - Knowledge base embeddings

2. **CloudWatch**
   - Fetch logs and metrics
   - Create and manage alarms

3. **S3**
   - Store analysis artifacts
   - Store uploaded files (logs, metrics, dashboards)

4. **DynamoDB**
   - Store knowledge base entries with vector embeddings
   - Enable semantic search

## Error Handling

The backend will implement a standardized error handling approach:

1. **HTTP Status Codes**
   - 400: Bad Request
   - 401: Unauthorized
   - 403: Forbidden
   - 404: Not Found
   - 500: Internal Server Error

2. **Error Response Format**
   ```json
   {
     "error": {
       "code": "ERROR_CODE",
       "message": "Human-readable error message",
       "details": {}
     }
   }
   ```

3. **Logging**
   - Structured logging with correlation IDs
   - Error tracking and monitoring

## Performance Considerations

1. **Asynchronous Processing**
   - Long-running analyses will be processed asynchronously
   - WebSocket notifications for analysis completion

2. **Caching**
   - Redis cache for frequently accessed data
   - Cache invalidation strategies

3. **Database Optimization**
   - Indexing for common queries
   - Connection pooling

## Deployment

The backend will be deployed to AWS Elastic Beanstalk with the following configuration:

1. **Docker Container**
   - Python 3.10 base image
   - FastAPI application
   - Gunicorn ASGI server

2. **Environment Variables**
   - Configuration for different environments (dev, staging, prod)
   - Secrets management

3. **Auto Scaling**
   - Scale based on CPU utilization
   - Min/max instance configuration

4. **Monitoring**
   - CloudWatch metrics and alarms
   - Health checks

## Next Steps

1. Set up the FastAPI project structure
2. Implement the core functionality
3. Implement the API endpoints
4. Implement the AWS Bedrock integration
5. Implement the authentication and authorization
6. Implement the database models
7. Implement the services
8. Write tests
9. Set up Docker containerization
10. Configure AWS Elastic Beanstalk deployment
