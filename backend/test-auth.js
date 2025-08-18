import axios from 'axios';

const BASE_URL = 'http://localhost:3000';

async function testAuth() {
  console.log('🔐 Testing PhishGuard Authentication...\n');

  try {
    // Test 1: Register a new user
    console.log('1. Testing User Registration...');
    const registerData = {
      firstName: 'Test',
      lastName: 'User',
      userName: 'testuser123',
      email: 'test@example.com',
      password: 'TestPassword123!'
    };

    const registerResponse = await axios.post(`${BASE_URL}/auth/register`, registerData);
    console.log('✅ Registration successful');
    console.log('   Token:', registerResponse.data.token ? 'Received' : 'Missing');
    console.log('   Message:', registerResponse.data.message);

    // Test 2: Login with the registered user
    console.log('\n2. Testing User Login...');
    const loginData = {
      email: 'test@example.com',
      password: 'TestPassword123!'
    };

    const loginResponse = await axios.post(`${BASE_URL}/auth/login`, loginData);
    console.log('✅ Login successful');
    console.log('   Token:', loginResponse.data.token ? 'Received' : 'Missing');
    console.log('   Message:', loginResponse.data.message);

    // Test 3: Test protected endpoint with token
    console.log('\n3. Testing Protected Endpoint...');
    const token = loginResponse.data.token;
    
    try {
      const protectedResponse = await axios.get(`${BASE_URL}/api/phishguard/health`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      console.log('✅ Protected endpoint accessible');
      console.log('   Status:', protectedResponse.data.status);
    } catch (error) {
      console.log('❌ Protected endpoint failed');
      console.log('   Error:', error.response?.data?.error || error.message);
    }

    // Test 4: Test without token (should fail)
    console.log('\n4. Testing Unprotected Access (should fail)...');
    try {
      await axios.get(`${BASE_URL}/api/phishguard/health`);
      console.log('❌ Should have failed without token');
    } catch (error) {
      if (error.response?.status === 401) {
        console.log('✅ Correctly blocked without token');
      } else {
        console.log('❌ Unexpected error:', error.response?.data?.error || error.message);
      }
    }

  } catch (error) {
    console.log('❌ Test failed:', error.response?.data?.error || error.message);
  }

  console.log('\n📋 Summary:');
  console.log('Backend should be running on: http://localhost:3000');
  console.log('Python service should be running on: http://localhost:8000');
  console.log('Frontend should be running on: http://localhost:3001');
}

// Run the test
testAuth().catch(console.error); 