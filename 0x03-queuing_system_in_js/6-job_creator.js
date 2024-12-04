import kue from 'kue';

const queue = kue.createQueue();

// Define the job data
const jobData = {
  phoneNumber: '123-456-7890',
  message: 'This is a test notification',
};

// Create a job in the "push_notification_code" queue
const job = queue.create('push_notification_code', jobData)
  .save((err) => {
    if (err) {
      console.log('Error creating notification job:', err);
    } else {
      console.log(`Notification job created: ${job.id}`);
    }
  });

// Listen for the job completion event
job.on('complete', () => {
  console.log('Notification job completed');
});

// Listen for the job failure event
job.on('failed', (errorMessage) => {
  console.log(`Notification job failed: ${errorMessage}`);
});
