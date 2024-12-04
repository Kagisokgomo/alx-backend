import { createClient } from 'redis';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Subscribe to the channel
client.subscribe('holberton school channel', (err, count) => {
  if (err) {
    console.log('Error subscribing to the channel:', err);
  } else {
    console.log(`Subscribed to ${count} channel(s).`);
  }
});

// Listen for messages on the subscribed channel
client.on('message', (channel, message) => {
  console.log(`Received message: ${message}`);
  if (message === 'KILL_SERVER') {
    console.log('Unsubscribing and quitting...');
    client.unsubscribe('holberton school channel');
    client.quit();
  }
});
