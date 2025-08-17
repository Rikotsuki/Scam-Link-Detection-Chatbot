import axios from 'axios';

const BACKEND_URL = 'http://localhost:3000';
const PYTHON_URL = 'http://localhost:8000';

async function testConnections() {
  console.log('🔍 Testing PhishGuard Service Connections...\n');

  // Test 1: Check if Express.js backend is running
  console.log('1. Testing Express.js Backend...');
  try {
    const backendResponse = await axios.get(`${BACKEND_URL}/api/phishguard/health`);
    console.log('✅ Express.js Backend: Running');
    console.log('   Status:', backendResponse.data.status);
    console.log('   Python Service:', backendResponse.data.python_service);
    console.log('   Message:', backendResponse.data.message);
  } catch (error) {
    console.log('❌ Express.js Backend: Not responding');
    console.log('   Error:', error.message);
  }

  console.log('\n2. Testing Python Service Directly...');
  try {
    const pythonResponse = await axios.get(`${PYTHON_URL}/`);
    console.log('✅ Python Service: Running');
    console.log('   Message:', pythonResponse.data.message);
    console.log('   Version:', pythonResponse.data.version);
  } catch (error) {
    console.log('❌ Python Service: Not responding');
    console.log('   Error:', error.message);
  }

  console.log('\n3. Testing API Endpoints...');
  
  // Test safety tips endpoint (no auth required)
  try {
    const tipsResponse = await axios.get(`${BACKEND_URL}/api/phishguard/tips`);
    console.log('✅ Safety Tips Endpoint: Working');
    console.log('   Tips Count:', tipsResponse.data.tips.length);
  } catch (error) {
    console.log('❌ Safety Tips Endpoint: Failed');
    console.log('   Error:', error.response?.data?.error || error.message);
  }

  // Test URL analysis endpoint (requires auth)
  try {
    const analysisResponse = await axios.post(`${BACKEND_URL}/api/phishguard/analyze`, {
      url: 'https://example.com'
    });
    console.log('✅ URL Analysis Endpoint: Working');
  } catch (error) {
    if (error.response?.status === 401) {
      console.log('✅ URL Analysis Endpoint: Working (requires authentication)');
    } else {
      console.log('❌ URL Analysis Endpoint: Failed');
      console.log('   Error:', error.response?.data?.error || error.message);
    }
  }

  console.log('\n📋 Summary:');
  console.log('Express.js Backend should be running on: http://localhost:3000');
  console.log('Python Service should be running on: http://localhost:8000');
  console.log('API Documentation: http://localhost:8000/docs');
  console.log('\nTo start services:');
  console.log('1. Python: cd ../python_services && python start_service.py');
  console.log('2. Backend: cd ../backend && npm run dev');
  console.log('3. Frontend: cd ../frontend && npm run dev');
}

// Run the test
testConnections().catch(console.error); 