import { createClient } from 'redis';

const client = createClient({
    url: 'redis://localhost:6379',
});

client.connect();

client.on('connect', () => {
    console.log('Connected to Redis');
});

client.on('error', (err) => {
    console.error('Redis connection error:', err);
});
