import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

// Create Redis client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Create Kue queue
const queue = kue.createQueue();

// Initialize express app
const app = express();
const port = 1245;

// Set the initial number of available seats to 50
setAsync('available_seats', 50);

// Set reservationEnabled to true
let reservationEnabled = true;

// Reserve a seat
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

// Get current available seats
async function getCurrentAvailableSeats() {
  const availableSeats = await getAsync('available_seats');
  return parseInt(availableSeats, 10);
}

// Route to get the available seats
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  // Create a job to reserve a seat
  const job = queue.create('reserve_seat', {})
    .save((err) => {
      if (err) {
        return res.json({ status: 'Reservation failed' });
      }
      res.json({ status: 'Reservation in process' });
    });
});

// Route to process the queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  // Process the jobs in the queue
  queue.process('reserve_seat', async (job, done) => {
    try {
      let availableSeats = await getCurrentAvailableSeats();

      if (availableSeats <= 0) {
        reservationEnabled = false;
        return done(new Error('Not enough seats available'));
      }

      // Reserve one seat
      availableSeats -= 1;
      await reserveSeat(availableSeats);

      console.log(`Seat reservation job ${job.id} completed`);
      done();
    } catch (err) {
      console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
      done(err);
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
