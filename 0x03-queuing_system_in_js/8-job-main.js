import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

// Create a Kue queue instance
const queue = kue.createQueue();

// List of jobs to be processed
const list = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  }
];

// Call the createPushNotificationsJobs function with the job list and queue
createPushNotificationsJobs(list, queue);
