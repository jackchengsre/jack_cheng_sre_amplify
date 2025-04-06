import requests
import json
import time
import os
from typing import Dict, Any, List, Optional

# Configuration
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

def test_backend_health():
    """Test the backend health endpoint"""
    print("Testing backend health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        response.raise_for_status()
        result = response.json()
        print(f"✅ Backend health check successful: {result}")
        return True
    except Exception as e:
        print(f"❌ Backend health check failed: {str(e)}")
        return False

def test_incidents_api():
    """Test the incidents API endpoints"""
    print("\nTesting incidents API...")
    
    # Get all incidents
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/incidents")
        response.raise_for_status()
        incidents = response.json()
        print(f"✅ Successfully retrieved {len(incidents)} incidents")
        
        if incidents:
            # Get a specific incident
            incident_id = incidents[0]["id"]
            response = requests.get(f"{BACKEND_URL}/api/v1/incidents/{incident_id}")
            response.raise_for_status()
            incident = response.json()
            print(f"✅ Successfully retrieved incident {incident_id}")
            
            # Create a new incident
            new_incident = {
                "title": "Test Incident",
                "description": "This is a test incident created by the end-to-end test script",
                "severity": "Low",
                "status": "Open",
                "services": ["Test Service"]
            }
            response = requests.post(f"{BACKEND_URL}/api/v1/incidents", json=new_incident)
            response.raise_for_status()
            created_incident = response.json()
            print(f"✅ Successfully created new incident {created_incident['id']}")
            
            # Update the incident
            update_data = {
                "title": "Updated Test Incident",
                "status": "Investigating"
            }
            response = requests.put(
                f"{BACKEND_URL}/api/v1/incidents/{created_incident['id']}", 
                json={**new_incident, **update_data}
            )
            response.raise_for_status()
            updated_incident = response.json()
            print(f"✅ Successfully updated incident {updated_incident['id']}")
            
            # Delete the incident
            response = requests.delete(f"{BACKEND_URL}/api/v1/incidents/{created_incident['id']}")
            response.raise_for_status()
            print(f"✅ Successfully deleted incident {created_incident['id']}")
        
        return True
    except Exception as e:
        print(f"❌ Incidents API test failed: {str(e)}")
        return False

def test_analysis_api():
    """Test the analysis API endpoints"""
    print("\nTesting analysis API...")
    
    try:
        # Get all analyses
        response = requests.get(f"{BACKEND_URL}/api/v1/analysis")
        response.raise_for_status()
        analyses = response.json()
        print(f"✅ Successfully retrieved {len(analyses)} analyses")
        
        # Get incidents to use for creating an analysis
        response = requests.get(f"{BACKEND_URL}/api/v1/incidents")
        response.raise_for_status()
        incidents = response.json()
        
        if incidents:
            # Create a new analysis
            new_analysis = {
                "incident_id": incidents[0]["id"],
                "type": "incident",
                "log_data": "2023-04-06T14:00:00Z INFO Starting application\n2023-04-06T14:01:00Z WARN High CPU usage detected\n2023-04-06T14:02:00Z ERROR ConnectionTimeoutException: Database connection timed out",
                "metrics_data": "CPU: 85%, Memory: 70%, Connections: 100/100"
            }
            response = requests.post(f"{BACKEND_URL}/api/v1/analysis", json=new_analysis)
            response.raise_for_status()
            created_analysis = response.json()
            print(f"✅ Successfully created new analysis {created_analysis['id']}")
            
            # Get the analysis
            response = requests.get(f"{BACKEND_URL}/api/v1/analysis/{created_analysis['id']}")
            response.raise_for_status()
            analysis = response.json()
            print(f"✅ Successfully retrieved analysis {analysis['id']}")
            
            # Test Bedrock analysis
            bedrock_request = {
                "incident_description": "API Gateway latency spike affecting product page loads",
                "log_data": "2023-04-06T14:00:00Z INFO Starting application\n2023-04-06T14:01:00Z WARN High CPU usage detected\n2023-04-06T14:02:00Z ERROR ConnectionTimeoutException: Database connection timed out",
                "metrics_data": "CPU: 85%, Memory: 70%, Connections: 100/100",
                "dashboard_data": "Dashboard shows connection pool maxed out at 14:02"
            }
            response = requests.post(f"{BACKEND_URL}/api/v1/bedrock/analyze", json=bedrock_request)
            response.raise_for_status()
            bedrock_analysis = response.json()
            print(f"✅ Successfully performed Bedrock analysis {bedrock_analysis['analysis_id']}")
        
        return True
    except Exception as e:
        print(f"❌ Analysis API test failed: {str(e)}")
        return False

def test_knowledge_api():
    """Test the knowledge base API endpoints"""
    print("\nTesting knowledge base API...")
    
    try:
        # Search knowledge base
        response = requests.get(f"{BACKEND_URL}/api/v1/knowledge")
        response.raise_for_status()
        entries = response.json()
        print(f"✅ Successfully retrieved {len(entries)} knowledge base entries")
        
        # Create a new knowledge base entry
        new_entry = {
            "title": "Test Knowledge Entry",
            "description": "This is a test knowledge base entry created by the end-to-end test script",
            "root_cause": "Test root cause",
            "resolution": "Test resolution",
            "services": ["Test Service"],
            "tags": ["test", "e2e"]
        }
        response = requests.post(f"{BACKEND_URL}/api/v1/knowledge", json=new_entry)
        response.raise_for_status()
        created_entry = response.json()
        print(f"✅ Successfully created new knowledge base entry {created_entry['id']}")
        
        # Get the entry
        response = requests.get(f"{BACKEND_URL}/api/v1/knowledge/{created_entry['id']}")
        response.raise_for_status()
        entry = response.json()
        print(f"✅ Successfully retrieved knowledge base entry {entry['id']}")
        
        # Update the entry
        update_data = {
            "title": "Updated Test Knowledge Entry",
            "tags": ["test", "e2e", "updated"]
        }
        response = requests.put(
            f"{BACKEND_URL}/api/v1/knowledge/{created_entry['id']}", 
            json={**new_entry, **update_data}
        )
        response.raise_for_status()
        updated_entry = response.json()
        print(f"✅ Successfully updated knowledge base entry {updated_entry['id']}")
        
        # Search with query
        response = requests.get(f"{BACKEND_URL}/api/v1/knowledge?query=updated")
        response.raise_for_status()
        search_results = response.json()
        print(f"✅ Successfully searched knowledge base with query 'updated', found {len(search_results)} results")
        
        # Delete the entry
        response = requests.delete(f"{BACKEND_URL}/api/v1/knowledge/{created_entry['id']}")
        response.raise_for_status()
        print(f"✅ Successfully deleted knowledge base entry {created_entry['id']}")
        
        return True
    except Exception as e:
        print(f"❌ Knowledge base API test failed: {str(e)}")
        return False

def test_cloudwatch_api():
    """Test the CloudWatch API endpoints"""
    print("\nTesting CloudWatch API...")
    
    try:
        # Get CloudWatch metrics
        metrics_request = {
            "namespace": "AWS/RDS",
            "metric_name": "CPUUtilization",
            "dimensions": {
                "DBInstanceIdentifier": "test-db"
            },
            "start_time": "2023-04-06T00:00:00Z",
            "end_time": "2023-04-06T23:59:59Z",
            "period": 300,
            "statistic": "Average"
        }
        response = requests.post(f"{BACKEND_URL}/api/v1/aws/cloudwatch/metrics", json=metrics_request)
        response.raise_for_status()
        metrics = response.json()
        print(f"✅ Successfully retrieved CloudWatch metrics with {len(metrics['Datapoints'])} datapoints")
        
        return True
    except Exception as e:
        print(f"❌ CloudWatch API test failed: {str(e)}")
        return False

def test_deployment_configs():
    """Test the deployment configuration files"""
    print("\nTesting deployment configuration files...")
    
    # Check frontend Amplify config
    amplify_config_path = "../frontend/amplify.yml"
    if os.path.exists(amplify_config_path):
        print(f"✅ Frontend Amplify configuration file exists")
    else:
        print(f"❌ Frontend Amplify configuration file not found at {amplify_config_path}")
        return False
    
    # Check backend Dockerfile
    dockerfile_path = "../backend/Dockerfile"
    if os.path.exists(dockerfile_path):
        print(f"✅ Backend Dockerfile exists")
    else:
        print(f"❌ Backend Dockerfile not found at {dockerfile_path}")
        return False
    
    # Check backend requirements.txt
    requirements_path = "../backend/requirements.txt"
    if os.path.exists(requirements_path):
        print(f"✅ Backend requirements.txt exists")
    else:
        print(f"❌ Backend requirements.txt not found at {requirements_path}")
        return False
    
    # Check backend Elastic Beanstalk config
    eb_config_path = "../backend/.ebextensions/01_fastapi.config"
    if os.path.exists(eb_config_path):
        print(f"✅ Backend Elastic Beanstalk configuration file exists")
    else:
        print(f"❌ Backend Elastic Beanstalk configuration file not found at {eb_config_path}")
        return False
    
    return True

def run_all_tests():
    """Run all end-to-end tests"""
    print("=== SRE Copilot End-to-End Tests ===\n")
    
    tests = [
        test_backend_health,
        test_incidents_api,
        test_analysis_api,
        test_knowledge_api,
        test_cloudwatch_api,
        test_deployment_configs
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n=== Test Summary ===")
    passed = results.count(True)
    failed = results.count(False)
    print(f"Passed: {passed}/{len(results)}")
    print(f"Failed: {failed}/{len(results)}")
    
    if failed == 0:
        print("\n✅ All tests passed! The SRE Copilot enhanced solution is ready for deployment.")
        return True
    else:
        print("\n❌ Some tests failed. Please review the logs above for details.")
        return False

if __name__ == "__main__":
    run_all_tests()
