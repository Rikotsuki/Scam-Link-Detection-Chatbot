// Backend configuration
export const config = {
  // Database
  DB_URL: process.env.DB_URL || 'mongodb://localhost:27017/phishguard',
  
  // JWT Configuration
  JWT_SECRET: process.env.JWT_SECRET || 'your_super_secret_jwt_key_here_change_this_in_production',
  JWT_EXPIRES_IN: process.env.JWT_EXPIRES_IN || '1d',
  
  // Python Service Configuration
  PYTHON_SERVICE_URL: process.env.PYTHON_SERVICE_URL || 'http://localhost:8000',
  PYTHON_SERVICE_PORT: process.env.PYTHON_SERVICE_PORT || '8000',
  
  // Server Configuration
  PORT: process.env.PORT || '3000'
}; 