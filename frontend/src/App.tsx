import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import Header from './components/layout/Header';
import Sidebar from './components/layout/Sidebar';
import HomePage from './pages/Home/HomePage';
import IncidentsPage from './pages/Incidents/IncidentsPage';
import AnalysisPage from './pages/Analysis/AnalysisPage';
import KnowledgeBasePage from './pages/KnowledgeBase/KnowledgeBasePage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import SettingsPage from './pages/Settings/SettingsPage';

const App: React.FC = () => {
  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <Header />
      <Sidebar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: 8,
          ml: { sm: 30 },
          overflow: 'auto'
        }}
      >
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/incidents" element={<IncidentsPage />} />
          <Route path="/analysis" element={<AnalysisPage />} />
          <Route path="/knowledge-base" element={<KnowledgeBasePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </Box>
    </Box>
  );
};

export default App;
