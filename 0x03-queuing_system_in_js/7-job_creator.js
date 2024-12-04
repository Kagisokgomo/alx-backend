import kue from 'kue';

// Create the Kue queue
const queue = kue.createQueue();

// Define the jobs array
const jobs = [
  { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
  { phoneNumber: '4153518781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4153518743', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4153538781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4153118782', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4153718781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4159518782', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4158718781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4153818782', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4154318781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4151218782', message: 'This is the code 4321 to verify your account' }
];

// Loop through the jobs array and create a job for each entry
jobs.forEach((jobData) => {
  const job = queue.create('push_notification_code_2', jobData)
    .save((err) => {
      if (err) {
        console.error('Notification job creation failed:', err);
      } else {
        console.log(`Notification job created: ${job.id}`);
      }
    });

  // Track job progress
  job.on('progress', (progress) => {
    console.log(`Notification job ${job.id} ${progress}% complete`);
  });

  // Track job completion
  job.on('complete', () => {
    console.log(`Notification job ${job.id} completed`);
  });

  // Track job failure
  job.on('failed', (err) => {
    console.log(`Notification job ${job.id} failed: ${err}`);
  });
});
