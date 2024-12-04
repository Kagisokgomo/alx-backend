import { createClient } from 'redis';

const client = createClient();

client.on('connect', function () {
  console.log('Redis client connected to the server');
});

client.on('error', function (err) {
  console.log('Something went wrong ' + err);
});

// Store hash values using hSet
const storeHashValues = async () => {
  try {
    // Use hSet to store hash values
    await client.hSet('HolbertonSchools', {
      Portland: 50,
      Seattle: 80,
      'New York': 20,
      Bogota: 20,
      Cali: 40,
      Paris: 2,
    });
    console.log('Hash values stored successfully');
  } catch (err) {
    console.error('Error storing hash values:', err);
  }
};

// Display stored hash values using hGetAll
const displayHashValues = async () => {
  try {
    const values = await client.hGetAll('HolbertonSchools');
    console.log(values);
  } catch (err) {
    console.error('Error fetching hash values:', err);
  }
};

// Execute the functions
const performRedisOperations = async () => {
  await storeHashValues();
  await displayHashValues();
};

// Run the operations
performRedisOperations().then(() => client.quit());
