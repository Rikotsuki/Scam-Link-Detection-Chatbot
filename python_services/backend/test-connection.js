import axios from 'axios';
import { configDotenv } from 'dotenv';

// Load environment variables
configDotenv();

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';
const AI_SERVICE_API_KEY = process.env.AI_SERVICE_API_KEY;

async function testAIServiceConnection() {
  console.log('🔍 Testing AI Service Connection...\n');

  try {
    // Test 1: Health Check
    console.log('1️⃣ Testing health check...');
    const healthResponse = await axios.get(`${AI_SERVICE_URL}/health`);
    console.log('✅ Health check passed:', healthResponse.data);
  } catch (error) {
    console.log('❌ Health check failed:', error.message);
  }

  try {
    // Test 2: URL Analysis
    console.log('\n2️⃣ Testing URL analysis...');
    const analysisResponse = await axios.post(
      `${AI_SERVICE_URL}/analyze`,
      {
        url: 'https://example.com',
        user_id: 'test-user',
        timestamp: new Date().toISOString(),
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${AI_SERVICE_API_KEY}`,
        },
      }
    );
    console.log('✅ URL analysis passed:', analysisResponse.data);
  } catch (error) {
    console.log('❌ URL analysis failed:', error.message);
    if (error.response) {
      console.log('Response data:', error.response.data);
    }
  }

  try {
    // Test 3: Chat Bot
    console.log('\n3️⃣ Testing chat bot...');
    const chatResponse = await axios.post(
      `${AI_SERVICE_URL}/chat`,
      {
        message: 'Hello, how can you help me?',
        session_id: 'test-session',
        user_id: 'test-user',
        timestamp: new Date().toISOString(),
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${AI_SERVICE_API_KEY}`,
        },
      }
    );
    console.log('✅ Chat bot passed:', chatResponse.data);
  } catch (error) {
    console.log('❌ Chat bot failed:', error.message);
    if (error.response) {
      console.log('Response data:', error.response.data);
    }
  }

  try {
    // Test 4: Safety Tips
    console.log('\n4️⃣ Testing safety tips...');
    const tipsResponse = await axios.get(`${AI_SERVICE_URL}/tips`);
    console.log('✅ Safety tips passed:', tipsResponse.data);
  } catch (error) {
    console.log('❌ Safety tips failed:', error.message);
  }

  console.log('\n🎯 Connection test completed!');
}

async function testExpressEndpoints() {
  console.log('\n🔍 Testing Express.js Endpoints...\n');

  const EXPRESS_URL = 'http://localhost:3000';

  try {
    // Test 1: Express Health Check
    console.log('1️⃣ Testing Express health check...');
    const healthResponse = await axios.get(`${EXPRESS_URL}/health`);
    console.log('✅ Express health check passed:', healthResponse.data);
  } catch (error) {
    console.log('❌ Express health check failed:', error.message);
  }

  try {
    // Test 2: AI Endpoint through Express
    console.log('\n2️⃣ Testing AI endpoint through Express...');
    const analysisResponse = await axios.post(
      `${EXPRESS_URL}/api/ai/analyze`,
      {
        url: 'https://example.com',
      }
    );
    console.log('✅ Express AI endpoint passed:', analysisResponse.data);
  } catch (error) {
    console.log('❌ Express AI endpoint failed:', error.message);
    if (error.response) {
      console.log('Response data:', error.response.data);
    }
  }

  try {
    // Test 3: AI Health through Express
    console.log('\n3️⃣ Testing AI health through Express...');
    const aiHealthResponse = await axios.get(`${EXPRESS_URL}/api/ai/health`);
    console.log('✅ Express AI health passed:', aiHealthResponse.data);
  } catch (error) {
    console.log('❌ Express AI health failed:', error.message);
  }

  console.log('\n🎯 Express endpoints test completed!');
}

// Run tests
async function runTests() {
  console.log('🚀 Starting PhishGuard Connection Tests...\n');
  
  await testAIServiceConnection();
  await testExpressEndpoints();
  
  console.log('\n✨ All tests completed!');
  console.log('\n📋 Summary:');
  console.log('- If you see ✅ marks, connections are working');
  console.log('- If you see ❌ marks, check your configuration');
  console.log('- Make sure both Python AI service and Express.js are running');
}

// Run the tests
runTests().catch(console.error); 