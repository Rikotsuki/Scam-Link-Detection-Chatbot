// API utility functions for communicating with the Express.js backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

// Generic API call function
async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    });

    const data = await response.json();

    if (!response.ok) {
      return { error: data.error || 'Request failed' };
    }

    return { data };
  } catch (error) {
    console.error('API call failed:', error);
    return { error: 'Network error' };
  }
}

// Authentication API calls
export const authApi = {
  register: async (userData: {
    firstName: string;
    lastName: string;
    userName: string;
    email: string;
    password: string;
  }) => {
    return apiCall<{ message: string; token: string }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  login: async (credentials: { email: string; password: string }) => {
    return apiCall<{ message: string; token: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },
};

// PhishGuard API calls
export const phishguardApi = {
  // Analyze a URL for phishing threats
  analyzeUrl: async (url: string, userId?: string) => {
    return apiCall<{
      url: string;
      is_suspicious: boolean;
      threat_level: string;
      message: string;
      confidence: number;
      detection_methods: string[];
      warnings: string[];
      analysis_time: number;
    }>('/api/phishguard/analyze', {
      method: 'POST',
      body: JSON.stringify({ url, user_id: userId }),
    });
  },

  // Report a scam URL
  reportScam: async (url: string, description: string, userId?: string) => {
    return apiCall<{
      success: boolean;
      message: string;
      report_id?: string;
    }>('/api/phishguard/report', {
      method: 'POST',
      body: JSON.stringify({ url, description, user_id: userId }),
    });
  },

  // Get safety tips
  getSafetyTips: async () => {
    return apiCall<{
      tips: string[];
      timestamp: string;
    }>('/api/phishguard/tips', {
      method: 'GET',
    });
  },

  // Chat with the bot (simple keyword-based responses)
  chatWithBot: async (message: string, userId?: string, sessionId?: string) => {
    return apiCall<{
      response: string;
      confidence: number;
      suggestions: string[];
      timestamp: string;
    }>('/api/phishguard/chat', {
      method: 'POST',
      body: JSON.stringify({ message, user_id: userId, session_id: sessionId }),
    });
  },

  // Health check
  healthCheck: async () => {
    return apiCall<{
      status: string;
      python_service: string;
      message: string;
    }>('/api/phishguard/health', {
      method: 'GET',
    });
  },
};

// Example usage in components:
/*
import { phishguardApi } from '@/lib/api';

// In a component:
const handleUrlAnalysis = async (url: string) => {
  const result = await phishguardApi.analyzeUrl(url);
  
  if (result.error) {
    console.error('Analysis failed:', result.error);
    return;
  }
  
  console.log('Analysis result:', result.data);
  // Handle the analysis result
};

const handleChat = async (message: string) => {
  const result = await phishguardApi.chatWithBot(message);
  
  if (result.error) {
    console.error('Chat failed:', result.error);
    return;
  }
  
  console.log('Bot response:', result.data);
  // Handle the bot response
};
*/ 