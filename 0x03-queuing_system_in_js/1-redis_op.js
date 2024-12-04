// 1-redis_op.js
const redis = require('redis');

// Connect to Redis server
const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Function to set a new school value in Redis
function setNewSchool(schoolName, value, callback) {
  client.set(schoolName, value, (err, reply) => {
    if (err) {
      console.error(err);
      return;
    }
    redis.print(null, reply);  // Ensure that the confirmation message is printed
    callback();  // Call the callback to proceed with the next operation
  });
}

// Function to display the value of a school from Redis
function displaySchoolValue(schoolName, callback) {
  client.get(schoolName, (err, reply) => {
    if (err) {
      console.error(err);
      return;
    }
    console.log(reply);
    callback();  // Call the callback to proceed with the next operation
  });
}

// Chain operations using callbacks to ensure proper sequence
displaySchoolValue('Holberton', () => {
  setNewSchool('HolbertonSanFrancisco', '100', () => {
    displaySchoolValue('HolbertonSanFrancisco', () => {
      // Only quit after all operations have completed
      client.quit();  
    });
  });
});
