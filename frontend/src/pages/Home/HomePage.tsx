import React, { useState } from 'react';
import { 
  Typography, 
  Box, 
  Card, 
  CardContent, 
  Grid, 
  Button, 
  Paper,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip
} from '@mui/material';
import { 
  Speed as SpeedIcon,
  Storage as StorageIcon,
  Memory as MemoryIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  
  const recentIncidents = [
    { id: 'INC-1234', title: 'API Gateway Latency Spike', severity: 'High', time: '2 hours ago' },
    { id: 'INC-1233', title: 'Database Connection Timeout', severity: 'Medium', time: '5 hours ago' },
    { id: 'INC-1232', title: 'Lambda Function Error Rate Increase', severity: 'Low', time: '1 day ago' }
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome to SRE Copilot
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Your AI-powered assistant for root cause analysis and incident management
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {/* Quick Actions */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Button 
                    variant="contained" 
                    fullWidth 
                    onClick={() => navigate('/analysis')}
                    sx={{ py: 2 }}
                  >
                    Start Analysis
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button 
                    variant="outlined" 
                    fullWidth 
                    onClick={() => navigate('/incidents')}
                    sx={{ py: 2 }}
                  >
                    View Incidents
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button 
                    variant="outlined" 
                    fullWidth 
                    onClick={() => navigate('/knowledge-base')}
                    sx={{ py: 2 }}
                  >
                    Knowledge Base
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button 
                    variant="outlined" 
                    fullWidth 
                    onClick={() => navigate('/dashboard')}
                    sx={{ py: 2 }}
                  >
                    Dashboard
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* System Status */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Status
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <List>
                <ListItem>
                  <ListItemIcon>
                    <SpeedIcon color="success" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="API Gateway" 
                    secondary="Latency: 45ms (p95)" 
                  />
                  <Chip label="Healthy" color="success" size="small" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <StorageIcon color="success" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Database" 
                    secondary="CPU: 32%, Connections: 85/100" 
                  />
                  <Chip label="Healthy" color="success" size="small" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <MemoryIcon color="warning" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Lambda Functions" 
                    secondary="Error Rate: 2.5%" 
                  />
                  <Chip label="Warning" color="warning" size="small" />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Incidents */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  Recent Incidents
                </Typography>
                <Button 
                  variant="text" 
                  onClick={() => navigate('/incidents')}
                >
                  View All
                </Button>
              </Box>
              <Divider sx={{ mb: 2 }} />
              
              <List>
                {recentIncidents.map((incident) => (
                  <Paper 
                    key={incident.id}
                    elevation={0}
                    sx={{ 
                      mb: 2, 
                      p: 2, 
                      border: '1px solid #e0e0e0',
                      borderRadius: 2,
                      '&:hover': {
                        boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
                        cursor: 'pointer'
                      }
                    }}
                    onClick={() => navigate(`/incidents/${incident.id}`)}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <WarningIcon 
                        color={
                          incident.severity === 'High' ? 'error' : 
                          incident.severity === 'Medium' ? 'warning' : 'info'
                        } 
                        sx={{ mr: 2 }}
                      />
                      <Box sx={{ flexGrow: 1 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                          <Typography variant="subtitle1">
                            {incident.title}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {incident.time}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
                          <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>
                            {incident.id}
                          </Typography>
                          <Chip 
                            label={incident.severity} 
                            size="small"
                            color={
                              incident.severity === 'High' ? 'error' : 
                              incident.severity === 'Medium' ? 'warning' : 'info'
                            }
                          />
                        </Box>
                      </Box>
                    </Box>
                  </Paper>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default HomePage;
