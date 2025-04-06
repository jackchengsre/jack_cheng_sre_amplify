import React, { useState } from 'react';
import { 
  Typography, 
  Box, 
  Card, 
  CardContent, 
  Grid, 
  Button, 
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Divider,
  Paper,
  Stepper,
  Step,
  StepLabel,
  CircularProgress,
  Alert
} from '@mui/material';
import { 
  Search as SearchIcon,
  CloudUpload as CloudUploadIcon
} from '@mui/icons-material';

const AnalysisPage: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [analysisComplete, setAnalysisComplete] = useState(false);
  const [analysisType, setAnalysisType] = useState('incident');
  const [incidentDescription, setIncidentDescription] = useState('');
  const [logData, setLogData] = useState('');
  const [metricsData, setMetricsData] = useState('');
  const [dashboardData, setDashboardData] = useState('');
  
  const steps = ['Configure Analysis', 'Provide Data', 'Review & Submit'];
  
  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };
  
  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };
  
  const handleSubmit = () => {
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
      setAnalysisComplete(true);
    }, 3000);
  };
  
  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Configure Analysis
            </Typography>
            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Analysis Type</InputLabel>
              <Select
                value={analysisType}
                label="Analysis Type"
                onChange={(e) => setAnalysisType(e.target.value)}
              >
                <MenuItem value="incident">Incident Analysis</MenuItem>
                <MenuItem value="performance">Performance Analysis</MenuItem>
                <MenuItem value="security">Security Analysis</MenuItem>
              </Select>
            </FormControl>
            
            <TextField
              label="Incident Description"
              multiline
              rows={4}
              fullWidth
              value={incidentDescription}
              onChange={(e) => setIncidentDescription(e.target.value)}
              placeholder="Describe the incident or issue you want to analyze..."
              sx={{ mb: 2 }}
            />
          </Box>
        );
      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Provide Data
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Card variant="outlined" sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      Log Data
                    </Typography>
                    <TextField
                      multiline
                      rows={4}
                      fullWidth
                      value={logData}
                      onChange={(e) => setLogData(e.target.value)}
                      placeholder="Paste log data or upload a log file..."
                      sx={{ mb: 2 }}
                    />
                    <Button
                      variant="outlined"
                      startIcon={<CloudUploadIcon />}
                      sx={{ mr: 1 }}
                    >
                      Upload Logs
                    </Button>
                    <Button
                      variant="outlined"
                      startIcon={<SearchIcon />}
                    >
                      Fetch from CloudWatch
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12}>
                <Card variant="outlined" sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      Metrics Data
                    </Typography>
                    <TextField
                      multiline
                      rows={4}
                      fullWidth
                      value={metricsData}
                      onChange={(e) => setMetricsData(e.target.value)}
                      placeholder="Paste metrics data or upload a metrics file..."
                      sx={{ mb: 2 }}
                    />
                    <Button
                      variant="outlined"
                      startIcon={<CloudUploadIcon />}
                      sx={{ mr: 1 }}
                    >
                      Upload Metrics
                    </Button>
                    <Button
                      variant="outlined"
                      startIcon={<SearchIcon />}
                    >
                      Fetch from CloudWatch
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      Dashboard Data
                    </Typography>
                    <TextField
                      multiline
                      rows={4}
                      fullWidth
                      value={dashboardData}
                      onChange={(e) => setDashboardData(e.target.value)}
                      placeholder="Paste dashboard data or upload dashboard screenshots..."
                      sx={{ mb: 2 }}
                    />
                    <Button
                      variant="outlined"
                      startIcon={<CloudUploadIcon />}
                    >
                      Upload Dashboard Screenshots
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Box>
        );
      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Review & Submit
            </Typography>
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Analysis Type: {analysisType === 'incident' ? 'Incident Analysis' : 
                               analysisType === 'performance' ? 'Performance Analysis' : 'Security Analysis'}
              </Typography>
              <Divider sx={{ my: 2 }} />
              <Typography variant="subtitle1" gutterBottom>
                Incident Description:
              </Typography>
              <Typography variant="body2" paragraph>
                {incidentDescription || 'No description provided'}
              </Typography>
              <Divider sx={{ my: 2 }} />
              <Typography variant="subtitle1" gutterBottom>
                Data Sources:
              </Typography>
              <Typography variant="body2">
                • Log Data: {logData ? 'Provided' : 'Not provided'}
              </Typography>
              <Typography variant="body2">
                • Metrics Data: {metricsData ? 'Provided' : 'Not provided'}
              </Typography>
              <Typography variant="body2">
                • Dashboard Data: {dashboardData ? 'Provided' : 'Not provided'}
              </Typography>
            </Paper>
            <Alert severity="info" sx={{ mb: 3 }}>
              The SRE Copilot will analyze your data using multiple specialized agents to identify the root cause of the issue.
            </Alert>
          </Box>
        );
      default:
        return null;
    }
  };
  
  const renderAnalysisResults = () => {
    return (
      <Box>
        <Alert severity="success" sx={{ mb: 3 }}>
          Analysis completed successfully!
        </Alert>
        
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Root Cause Analysis
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Typography variant="body1" paragraph>
              The root cause of the incident appears to be a connection pool exhaustion in the database layer. 
              The application was making more concurrent connections than the configured maximum, leading to connection timeouts.
            </Typography>
            <Typography variant="body1" paragraph>
              This was triggered by a sudden increase in traffic to the API Gateway, which propagated to the database layer.
              The metrics show a 300% increase in request rate starting at 14:00 UTC, which correlates with the beginning of the incident.
            </Typography>
          </CardContent>
        </Card>
        
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Recommended Actions
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Typography variant="body1" component="div">
              <ol>
                <li>Increase the database connection pool size from 100 to at least 250 connections</li>
                <li>Implement connection pooling at the application level to better manage database connections</li>
                <li>Add rate limiting to the API Gateway to prevent sudden traffic spikes</li>
                <li>Set up CloudWatch alarms for database connection usage (alert at 80% capacity)</li>
              </ol>
            </Typography>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Similar Past Incidents
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Typography variant="body2" paragraph>
              <strong>INC-1098 (2 months ago):</strong> Similar connection pool exhaustion during a marketing campaign launch
            </Typography>
            <Typography variant="body2" paragraph>
              <strong>INC-876 (6 months ago):</strong> Database connection issues during peak traffic hours
            </Typography>
          </CardContent>
        </Card>
        
        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
          <Button 
            variant="outlined"
            onClick={() => {
              setAnalysisComplete(false);
              setActiveStep(0);
            }}
          >
            Start New Analysis
          </Button>
          <Button 
            variant="contained"
            onClick={() => {
              // Save to knowledge base logic would go here
              alert('Analysis saved to knowledge base');
            }}
          >
            Save to Knowledge Base
          </Button>
        </Box>
      </Box>
    );
  };
  
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Multi-Modal Analysis
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Analyze incidents using logs, metrics, and dashboard data to identify root causes
      </Typography>
      
      {!analysisComplete ? (
        <>
          <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
          
          <Box sx={{ mt: 2, mb: 4 }}>
            {renderStepContent(activeStep)}
          </Box>
          
          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <Button
              variant="outlined"
              disabled={activeStep === 0}
              onClick={handleBack}
            >
              Back
            </Button>
            <Box>
              {activeStep === steps.length - 1 ? (
                <Button
                  variant="contained"
                  onClick={handleSubmit}
                  disabled={loading}
                  startIcon={loading && <CircularProgress size={20} />}
                >
                  {loading ? 'Analyzing...' : 'Start Analysis'}
                </Button>
              ) : (
                <Button
                  variant="contained"
                  onClick={handleNext}
                >
                  Next
                </Button>
              )}
            </Box>
          </Box>
        </>
      ) : (
        renderAnalysisResults()
      )}
    </Box>
  );
};

export default AnalysisPage;
