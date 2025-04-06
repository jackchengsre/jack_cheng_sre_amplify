import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, Avatar, Badge, Box } from '@mui/material';
import { Notifications as NotificationsIcon, Settings as SettingsIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const Header: React.FC = () => {
  const navigate = useNavigate();

  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <img 
            src="/logo.svg" 
            alt="SRE Copilot Logo" 
            style={{ height: 40, marginRight: 16 }} 
          />
          <Typography variant="h6" noWrap component="div">
            SRE Copilot
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex' }}>
          <IconButton 
            size="large" 
            color="inherit"
            onClick={() => navigate('/notifications')}
          >
            <Badge badgeContent={4} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>
          
          <IconButton 
            size="large" 
            color="inherit"
            onClick={() => navigate('/settings')}
          >
            <SettingsIcon />
          </IconButton>
          
          <IconButton 
            size="large" 
            sx={{ ml: 1 }}
            onClick={() => navigate('/profile')}
          >
            <Avatar sx={{ width: 32, height: 32 }}>U</Avatar>
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
