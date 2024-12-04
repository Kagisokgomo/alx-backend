import kue from 'kue';

// Function to create push notification jobs
function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  jobs.forEach((jobData) => {
    // Create a new job in the queue
    const job = queue.create('push_notification_code_3', jobData)
      .save((err) => {
        if (err) {
          console.error(`Notification job creation failed: ${err}`);
        } else {
          console.log(`Notification job created: ${job.id}`);
        }
      });

    // Job progress event listener
    job.on('progress', (progress) => {
      console.log(`Notification job #${job.id} ${progress}% complete`);
    });

    // Job completion event listener
    job.on('complete', () => {
      console.log(`Notification job #${job.id} completed`);
    });

    // Job failure event listener
    job.on('failed', (errorMessage) => {
      console.log(`Notification job #${job.id} failed: ${errorMessage}`);
    });
  });
}

export default createPushNotificationsJobs;
