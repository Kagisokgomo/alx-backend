import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

// Create a queue instance
const queue = kue.createQueue();

describe('createPushNotificationsJobs', function() {
  // Set up test mode
  beforeEach(() => {
    queue.testMode = true;  // Enable test mode to prevent job processing
  });

  // Clear the queue after tests
  afterEach(() => {
    queue.testMode = false;  // Disable test mode
    queue.shutdown(500, (err) => {  // Clean up the queue
      if (err) console.error('Error during queue shutdown', err);
    });
  });

  it('should display an error message if jobs is not an array', function() {
    try {
      createPushNotificationsJobs({}, queue);  // Passing a non-array value
    } catch (error) {
      expect(error.message).to.equal('Jobs is not an array');
    }
  });

  it('should create two new jobs in the queue', function() {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account',
      },
    ];

    createPushNotificationsJobs(jobs, queue);

    // Validate that two jobs are in the queue
    const jobIds = queue.testMode.jobs('push_notification_code_3');
    expect(jobIds.length).to.equal(2);

    // Validate job details for each job
    const job = queue.testMode.get(jobIds[0]);
    expect(job.data.phoneNumber).to.equal('4153518780');
    expect(job.data.message).to.equal('This is the code 1234 to verify your account');
  });

  it('should handle job events correctly (job creation, completion, and failure)', function(done) {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
    ];

    const job = queue.create('push_notification_code_3', jobs[0]);

    job
      .on('complete', (result) => {
        console.log(`Notification job #${job.id} completed`);
        expect(result).to.equal(undefined); // Check for completion status (modify as per job result)
      })
      .on('failed', (err) => {
        console.error(`Notification job #${job.id} failed: ${err}`);
      })
      .on('progress', (progress) => {
        console.log(`Notification job #${job.id} ${progress}% complete`);
      });

    createPushNotificationsJobs(jobs, queue);

    done();
  });
});
