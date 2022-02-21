const createQueue = async (AWS, queueName, topicARN) => {
	try {
		const sqs = new AWS.SQS({ apiVersion: '2012-11-05' });
		const params = {
			QueueName: queueName,
			Attributes: {
				Policy: `{
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "",
                            "Effect": "Allow",
                            "Principal": {
                                "AWS": "*"
                            },
                            "Action": "SQS:SendMessage",
                            "Resource": "arn:aws:sqs:us-west-2:${process.env.USER_ACCESS_KEY}:${queueName}",
                            "Condition": {
                                "ArnEquals": {
                                    "aws:SourceArn": "${topicARN}"
                                }
                            }
                        }]
                    }`,
			},
		};

		const queueData = await sqs.createQueue(params).promise();
		const queueARN = await sqs
			.getQueueAttributes({
				QueueUrl: queueData.QueueUrl,
				AttributeNames: ['QueueArn'],
			})
			.promise();
		return queueARN.Attributes.QueueArn;
	} catch (err) {
		console.log(err);
		return -1;
	}
};

const subscribeSQS = async (AWS, protocol, endpoint, topicARN) => {
	try {
		const sns = new AWS.SNS({ apiVersion: '2010-03-31' });

		const params = {
			Protocol: protocol,
			TopicArn: topicARN,
			Endpoint: endpoint,
		};
		const subscribeData = await sns.subscribe(params).promise();
		return subscribeData;
	} catch (err) {
		return -1;
	}
};

module.exports = { createQueue, subscribeSQS };
