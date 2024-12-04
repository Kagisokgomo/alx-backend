import kue from 'kue';

// Create the Kue queue
const queue = kue.createQueue();

// Array of blacklisted phone numbers
const blacklistedNumbers = [
  '4153518780',
  '4153518781'
];

// Function to send notification
function sendNotification(phoneNumber, message, job, done) {
  // Track job progress from 0%
  job.progress(0, 100);

  // Check if the phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    // Fail the job if the number is blacklisted
    job.fail(new Error(`Phone number ${phoneNumber} is blacklisted`));
    job.save(() => {
      done(new Error(`Phone number ${phoneNumber} is blacklisted`));
    });
  } else {
    // Track progress to 50%
    job.progress(50, 100);
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

    // Simulate sending the notification
    setTimeout(() => {
      console.log(`Notification sent to ${phoneNumber}: ${message}`);
      job.complete();
      done();
    }, 1000); // Simulate async behavior
  }
}

// Process jobs from the queue
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});

// Monitor job completion and failure
queue.on('job complete', (id) => {
  console.log(`Notification job #${id} completed`);
});

queue.on('job failed', (id, errorMessage) => {
  console.log(`Notification job #${id} failed: ${errorMessage}`);
});

queue.on('job progress', (id, progress) => {
  console.log(`Notification job #${id} ${progress}% complete`);
});
