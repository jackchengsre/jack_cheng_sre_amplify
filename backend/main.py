from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import json

# Initialize FastAPI app
app = FastAPI(
    title="SRE Copilot API",
    description="API for SRE Copilot - AI-powered root cause analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class IncidentBase(BaseModel):
    title: str
    description: str
    severity: str
    status: str
    services: List[str]

class IncidentCreate(IncidentBase):
    pass

class Incident(IncidentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AnalysisBase(BaseModel):
    incident_id: str
    type: str
    log_data: Optional[str] = None
    metrics_data: Optional[str] = None
    dashboard_data: Optional[str] = None

class AnalysisCreate(AnalysisBase):
    pass

class Analysis(AnalysisBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    result: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class KnowledgeBaseEntryBase(BaseModel):
    title: str
    description: str
    root_cause: str
    resolution: str
    services: List[str]
    tags: List[str]

class KnowledgeBaseEntryCreate(KnowledgeBaseEntryBase):
    pass

class KnowledgeBaseEntry(KnowledgeBaseEntryBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Mock database
incidents_db = {}
analyses_db = {}
knowledge_db = {}

# Incident endpoints
@app.get("/api/v1/incidents", response_model=List[Incident])
async def list_incidents():
    return list(incidents_db.values())

@app.get("/api/v1/incidents/{incident_id}", response_model=Incident)
async def get_incident(incident_id: str):
    if incident_id not in incidents_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incidents_db[incident_id]

@app.post("/api/v1/incidents", response_model=Incident, status_code=status.HTTP_201_CREATED)
async def create_incident(incident: IncidentCreate):
    incident_id = str(uuid.uuid4())
    now = datetime.utcnow()
    new_incident = Incident(
        id=incident_id,
        created_at=now,
        updated_at=now,
        **incident.dict()
    )
    incidents_db[incident_id] = new_incident
    return new_incident

@app.put("/api/v1/incidents/{incident_id}", response_model=Incident)
async def update_incident(incident_id: str, incident: IncidentCreate):
    if incident_id not in incidents_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    stored_incident = incidents_db[incident_id]
    update_data = incident.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(stored_incident, field, value)
    
    stored_incident.updated_at = datetime.utcnow()
    incidents_db[incident_id] = stored_incident
    return stored_incident

@app.delete("/api/v1/incidents/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_incident(incident_id: str):
    if incident_id not in incidents_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    del incidents_db[incident_id]
    return None

# Analysis endpoints
@app.get("/api/v1/analysis", response_model=List[Analysis])
async def list_analyses():
    return list(analyses_db.values())

@app.get("/api/v1/analysis/{analysis_id}", response_model=Analysis)
async def get_analysis(analysis_id: str):
    if analysis_id not in analyses_db:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analyses_db[analysis_id]

@app.post("/api/v1/analysis", response_model=Analysis, status_code=status.HTTP_201_CREATED)
async def create_analysis(analysis: AnalysisCreate):
    if analysis.incident_id not in incidents_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    analysis_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    # In a real implementation, this would trigger an asynchronous analysis job
    # For now, we'll simulate a completed analysis with mock results
    mock_result = {
        "root_cause": "Connection pool exhaustion in the database layer",
        "confidence": 0.92,
        "findings": [
            "Database connection pool reached maximum capacity (100/100)",
            "Sudden 300% increase in traffic to API Gateway at 14:00 UTC",
            "No rate limiting configured on API endpoints"
        ],
        "recommendations": [
            "Increase connection pool size from 100 to 250",
            "Implement connection pooling at application level",
            "Add rate limiting to API Gateway",
            "Set up CloudWatch alarms for connection usage"
        ],
        "similar_incidents": [
            {"id": "INC-1098", "title": "Database connection timeout during marketing campaign", "similarity": 0.87},
            {"id": "INC-876", "title": "Connection issues during peak hours", "similarity": 0.72}
        ]
    }
    
    new_analysis = Analysis(
        id=analysis_id,
        status="completed",  # In real implementation, would start as "pending"
        created_at=now,
        updated_at=now,
        result=mock_result,
        **analysis.dict()
    )
    
    analyses_db[analysis_id] = new_analysis
    return new_analysis

# Knowledge Base endpoints
@app.get("/api/v1/knowledge", response_model=List[KnowledgeBaseEntry])
async def search_knowledge_base(query: Optional[str] = None):
    entries = list(knowledge_db.values())
    
    if query:
        # In a real implementation, this would use vector similarity search
        # For now, we'll do a simple text search
        filtered_entries = []
        for entry in entries:
            if (query.lower() in entry.title.lower() or 
                query.lower() in entry.description.lower() or
                query.lower() in entry.root_cause.lower()):
                filtered_entries.append(entry)
        return filtered_entries
    
    return entries

@app.get("/api/v1/knowledge/{entry_id}", response_model=KnowledgeBaseEntry)
async def get_knowledge_base_entry(entry_id: str):
    if entry_id not in knowledge_db:
        raise HTTPException(status_code=404, detail="Knowledge base entry not found")
    return knowledge_db[entry_id]

@app.post("/api/v1/knowledge", response_model=KnowledgeBaseEntry, status_code=status.HTTP_201_CREATED)
async def create_knowledge_base_entry(entry: KnowledgeBaseEntryCreate):
    entry_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    new_entry = KnowledgeBaseEntry(
        id=entry_id,
        created_at=now,
        updated_at=now,
        **entry.dict()
    )
    
    knowledge_db[entry_id] = new_entry
    return new_entry

@app.put("/api/v1/knowledge/{entry_id}", response_model=KnowledgeBaseEntry)
async def update_knowledge_base_entry(entry_id: str, entry: KnowledgeBaseEntryCreate):
    if entry_id not in knowledge_db:
        raise HTTPException(status_code=404, detail="Knowledge base entry not found")
    
    stored_entry = knowledge_db[entry_id]
    update_data = entry.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(stored_entry, field, value)
    
    stored_entry.updated_at = datetime.utcnow()
    knowledge_db[entry_id] = stored_entry
    return stored_entry

@app.delete("/api/v1/knowledge/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge_base_entry(entry_id: str):
    if entry_id not in knowledge_db:
        raise HTTPException(status_code=404, detail="Knowledge base entry not found")
    
    del knowledge_db[entry_id]
    return None

# AWS Bedrock integration endpoint
class BedrockAnalysisRequest(BaseModel):
    incident_description: str
    log_data: Optional[str] = None
    metrics_data: Optional[str] = None
    dashboard_data: Optional[str] = None

class BedrockAnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    result: Optional[Dict[str, Any]] = None

@app.post("/api/v1/bedrock/analyze", response_model=BedrockAnalysisResponse)
async def analyze_with_bedrock(request: BedrockAnalysisRequest):
    # In a real implementation, this would call AWS Bedrock models
    # For now, we'll simulate a response
    
    analysis_id = str(uuid.uuid4())
    
    # Mock result from AWS Bedrock
    mock_result = {
        "supervisor_analysis": {
            "root_cause": "The root cause appears to be a connection pool exhaustion in the database layer, triggered by a sudden traffic spike.",
            "confidence": 0.94,
            "contributing_factors": [
                "Insufficient connection pool size",
                "No rate limiting on API",
                "Lack of connection pooling at application level"
            ]
        },
        "log_analysis": {
            "model": "Claude 3 Haiku",
            "key_findings": [
                "Multiple 'ConnectionTimeoutException' errors starting at 14:02 UTC",
                "Database connection pool reached maximum capacity (100/100) at 14:03 UTC",
                "Error rate increased from 0.1% to 4.5% within 5 minutes"
            ]
        },
        "metrics_analysis": {
            "model": "Amazon Titan Text",
            "key_findings": [
                "API request rate increased by 300% at 14:00 UTC",
                "Database CPU utilization spiked to 85% at 14:01 UTC",
                "Response time increased from 120ms to 2300ms"
            ]
        },
        "dashboard_analysis": {
            "model": "Amazon Nova Lite",
            "key_findings": [
                "Dashboard shows clear correlation between traffic spike and error rate",
                "Connection pool utilization graph shows plateau at maximum capacity",
                "Similar pattern observed in previous incidents (INC-1098, INC-876)"
            ]
        }
    }
    
    return BedrockAnalysisResponse(
        analysis_id=analysis_id,
        status="completed",
        result=mock_result
    )

# CloudWatch integration endpoint
class CloudWatchMetricsRequest(BaseModel):
    namespace: str
    metric_name: str
    dimensions: Dict[str, str]
    start_time: datetime
    end_time: datetime
    period: int = 60
    statistic: str = "Average"

@app.post("/api/v1/aws/cloudwatch/metrics")
async def get_cloudwatch_metrics(request: CloudWatchMetricsRequest):
    # In a real implementation, this would call CloudWatch API
    # For now, we'll return mock data
    
    # Generate mock time series data
    start_timestamp = int(request.start_time.timestamp())
    end_timestamp = int(request.end_time.timestamp())
    step = request.period
    
    datapoints = []
    current = start_timestamp
    
    import random
    
    while current <= end_timestamp:
        # Generate realistic-looking metrics with some randomness
        if request.metric_name == "CPUUtilization":
            value = 30 + random.random() * 20
            # Add a spike for demonstration
            if current > start_timestamp + (end_timestamp - start_timestamp) * 0.7:
                value += 30
        elif request.metric_name == "DatabaseConnections":
            value = 50 + random.random() * 20
            # Add a spike for demonstration
            if current > start_timestamp + (end_timestamp - start_timestamp) * 0.7:
                value = 100  # Max connections
        else:
            value = random.random() * 100
            
        datapoints.append({
            "Timestamp": datetime.fromtimestamp(current).isoformat(),
            "Value": value,
            "Unit": "Count" if request.metric_name == "DatabaseConnections" else "Percent"
        })
        
        current += step
    
    return {
        "Namespace": request.namespace,
        "MetricName": request.metric_name,
        "Dimensions": [{"Name": k, "Value": v} for k, v in request.dimensions.items()],
        "Datapoints": datapoints
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Add some sample data
def add_sample_data():
    # Sample incidents
    incidents = [
        {
            "id": "INC-1234",
            "title": "API Gateway Latency Spike",
            "description": "Our e-commerce website is experiencing high latency (>2s) for product page loads since 2:00 PM today.",
            "severity": "High",
            "status": "Open",
            "services": ["API Gateway", "Lambda", "DynamoDB"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "INC-1233",
            "title": "Database Connection Timeout",
            "description": "Users are reporting intermittent errors when trying to save data. Database connection timeouts observed in logs.",
            "severity": "Medium",
            "status": "Investigating",
            "services": ["RDS", "Application Server"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "INC-1232",
            "title": "Lambda Function Error Rate Increase",
            "description": "Error rate for the order processing Lambda function increased from 0.1% to 3% in the last hour.",
            "severity": "Low",
            "status": "Resolved",
            "services": ["Lambda", "SQS"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    for incident in incidents:
        incident_id = incident.pop("id")
        incidents_db[incident_id] = Incident(id=incident_id, **incident)
    
    # Sample knowledge base entries
    knowledge_entries = [
        {
            "id": "KB-001",
            "title": "API Gateway Latency Issues",
            "description": "High latency in API Gateway affecting product page loads",
            "root_cause": "API Gateway throttling due to reaching account limits",
            "resolution": "Increased API Gateway account limits and implemented caching",
            "services": ["API Gateway", "CloudFront"],
            "tags": ["latency", "throttling", "api-gateway"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "KB-002",
            "title": "Database Connection Pool Exhaustion",
            "description": "Users experiencing errors when saving data due to database connection timeouts",
            "root_cause": "Connection pool exhaustion during traffic spikes",
            "resolution": "Increased connection pool size and implemented connection pooling at application level",
            "services": ["RDS", "Application Server"],
            "tags": ["database", "connection-pool", "timeout"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    for entry in knowledge_entries:
        entry_id = entry.pop("id")
        knowledge_db[entry_id] = KnowledgeBaseEntry(id=entry_id, **entry)

# Add sample data on startup
@app.on_event("startup")
async def startup_event():
    add_sample_data()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
