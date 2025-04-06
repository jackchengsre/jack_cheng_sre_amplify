import axios from 'axios';

// Base API URL - would be configured based on environment
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors (401, 403, etc.)
    if (error.response) {
      if (error.response.status === 401) {
        // Handle unauthorized (e.g., redirect to login)
        localStorage.removeItem('auth_token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Incidents API
export const incidentsApi = {
  getAll: async () => {
    const response = await apiClient.get('/api/v1/incidents');
    return response.data;
  },
  
  getById: async (id) => {
    const response = await apiClient.get(`/api/v1/incidents/${id}`);
    return response.data;
  },
  
  create: async (incidentData) => {
    const response = await apiClient.post('/api/v1/incidents', incidentData);
    return response.data;
  },
  
  update: async (id, incidentData) => {
    const response = await apiClient.put(`/api/v1/incidents/${id}`, incidentData);
    return response.data;
  },
  
  delete: async (id) => {
    await apiClient.delete(`/api/v1/incidents/${id}`);
    return true;
  }
};

// Analysis API
export const analysisApi = {
  getAll: async () => {
    const response = await apiClient.get('/api/v1/analysis');
    return response.data;
  },
  
  getById: async (id) => {
    const response = await apiClient.get(`/api/v1/analysis/${id}`);
    return response.data;
  },
  
  create: async (analysisData) => {
    const response = await apiClient.post('/api/v1/analysis', analysisData);
    return response.data;
  },
  
  analyzeWithBedrock: async (analysisData) => {
    const response = await apiClient.post('/api/v1/bedrock/analyze', analysisData);
    return response.data;
  }
};

// Knowledge Base API
export const knowledgeApi = {
  search: async (query = '') => {
    const response = await apiClient.get('/api/v1/knowledge', {
      params: { query }
    });
    return response.data;
  },
  
  getById: async (id) => {
    const response = await apiClient.get(`/api/v1/knowledge/${id}`);
    return response.data;
  },
  
  create: async (entryData) => {
    const response = await apiClient.post('/api/v1/knowledge', entryData);
    return response.data;
  },
  
  update: async (id, entryData) => {
    const response = await apiClient.put(`/api/v1/knowledge/${id}`, entryData);
    return response.data;
  },
  
  delete: async (id) => {
    await apiClient.delete(`/api/v1/knowledge/${id}`);
    return true;
  }
};

// CloudWatch API
export const cloudwatchApi = {
  getMetrics: async (metricsRequest) => {
    const response = await apiClient.post('/api/v1/aws/cloudwatch/metrics', metricsRequest);
    return response.data;
  }
};

// Health check
export const healthApi = {
  check: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  }
};

export default {
  incidents: incidentsApi,
  analysis: analysisApi,
  knowledge: knowledgeApi,
  cloudwatch: cloudwatchApi,
  health: healthApi
};
