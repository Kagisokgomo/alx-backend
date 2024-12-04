import kue from 'kue';

// Create the Kue queue
const queue = kue.createQueue();

// Define the function that processes the job
function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// Create a job processor for the "push_notification_code" queue
queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;

  // Call sendNotification with the job data
  sendNotification(phoneNumber, message);

  // Mark the job as completed
  done();
});
