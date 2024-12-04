// 2-redis_op_async.js
const redis = require('redis');
const { promisify } = require('util');

// Connect to Redis server
const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Promisify the Redis methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Function to set a new school value in Redis using async/await
async function setNewSchool(schoolName, value) {
  try {
    const reply = await setAsync(schoolName, value);
    console.log(reply);  // Display the confirmation message
  } catch (err) {
    console.error(err);
  }
}

// Function to display the value of a school from Redis using async/await
async function displaySchoolValue(schoolName) {
  try {
    const reply = await getAsync(schoolName);
    console.log(reply);  // Log the retrieved value
  } catch (err) {
    console.error(err);
  }
}

// Async function to chain operations
async function performRedisOperations() {
  try {
    await displaySchoolValue('Holberton');  // Display the value of 'Holberton'
    await setNewSchool('HolbertonSanFrancisco', '100');  // Set a new school value
    await displaySchoolValue('HolbertonSanFrancisco');  // Display the value of 'HolbertonSanFrancisco'
  } catch (err) {
    console.error('Error in Redis operations:', err);
  } finally {
    // Quit the Redis client after all operations are complete
    client.quit();
  }
}

// Perform the operations
performRedisOperations();
