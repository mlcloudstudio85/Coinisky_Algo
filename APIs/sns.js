const express = require('express');
const router = express.Router();
const AWS = require('aws-sdk');
const { createQueue, subscribeSQS } = require('../utils/notifications');

const awsCredentials = {
	region: 'us-west-2',
	accessKeyId: process.env.USER_ACCESS_KEY,
	secretAccessKey: process.env.USER_SECRET_KEY,
};
AWS.config.update(awsCredentials);

router.post('/create', async function (req, res) {
	try {
		const { topicName } = req.body;
		const sns = new AWS.SNS({ apiVersion: '2010-03-31' });
		const params = {
			Name: topicName,
		};
		sns.createTopic(params, async function (err, data) {
			if (err) {
				return res.json({
					message: 'topic not created',
					error: err,
				});
			} else {
				const topicARN = data.TopicArn;
				const queueName = `${topicName}-queue`;

				const queueARN = await createQueue(AWS, queueName, topicARN);
				if (!queueARN || queueARN === -1) throw 'queue not created';
				const subscribeData = await subscribeSQS(
					AWS,
					'sqs',
					queueARN,
					topicARN
				);
				if (!subscribeData || subscribeData === -1)
					throw 'subscription not created';
				return res.json({
					message: 'topic created',
					result: data,
				});
			}
		});
	} catch (err) {
		return res.json({
			message: 'topic not created',
			error: err,
		});
	}
});

router.get('/list', async function (req, res) {
	try {
		const sns = new AWS.SNS({ apiVersion: '2010-03-31' });
		const params = {
			// NextToken: 'STRING_VALUE',
			// MaxItems: 0
		};
		sns.listTopics(params, function (err, data) {
			if (err) {
				return res.json({
					message: 'topics not listed',
					error: err,
				});
			} else {
				return res.json({
					message: 'topics listed',
					result: data,
				});
			}
		});
	} catch (err) {
		return res.json({
			message: 'topics not listed',
			error: err,
		});
	}
});

router.delete('/delete', async function (req, res) {
	try {
		const { topicArn } = req.body;
		const sns = new AWS.SNS({ apiVersion: '2010-03-31' });
		const params = {
			TopicArn: topicArn,
		};
		sns.deleteTopic(params, function (err, data) {
			if (err) {
				return res.json({
					message: 'topic not deleted',
					error: err,
				});
			} else {
				return res.json({
					message: 'topic deleted',
					result: data,
				});
			}
		});
	} catch (err) {
		return res.json({
			message: 'topic not deleted',
			error: err,
		});
	}
});

router.post('/subscribe', async function (req, res) {
	try {
		const { topicArn, email } = req.body;
		const sns = new AWS.SNS({ apiVersion: '2010-03-31' });
		const params = {
			Protocol: 'email',
			TopicArn: topicArn,
			Endpoint: email,
		};
		sns.subscribe(params, function (err, data) {
			if (err) {
				return res.json({
					message: 'subscription not created',
					error: err,
				});
			} else {
				return res.json({
					message: 'subscription created',
					result: data,
				});
			}
		});
	} catch (err) {
		return res.json({
			message: 'subscription not created',
			error: err,
		});
	}
});

router.get('/subscriptions', async function (req, res) {
	try {
		const { topicArn } = req.body;
		const sns = new AWS.SNS({ apiVersion: '2010-03-31' });
		const params = {
			TopicArn: topicArn,
		};
		sns.listSubscriptionsByTopic(params, function (err, data) {
			if (err) {
				return res.json({
					message: 'subscriptions not listed',
					error: err,
				});
			} else {
				return res.json({
					message: 'subscriptions listed',
					result: data,
				});
			}
		});
	} catch (err) {
		return res.json({
			message: 'subscriptions not listed',
			error: err,
		});
	}
});

router.post('/unsubscribe', async function (req, res) {
	try {
		const { subscriptionArn } = req.body;
		const sns = new AWS.SNS({ apiVersion: '2010-03-31' });
		const params = {
			SubscriptionArn: subscriptionArn,
		};
		sns.unsubscribe(params, function (err, data) {
			if (err) {
				return res.json({
					message: 'subscription not deleted',
					error: err,
				});
			} else {
				return res.json({
					message: 'subscription deleted',
					result: data,
				});
			}
		});
	} catch (err) {
		return res.json({
			message: 'subscription not deleted',
			error: err,
		});
	}
});

router.post('/publish', async function (req, res) {
	try {
		const { topicArn, subject, message } = req.body;
		const sns = new AWS.SNS({ apiVersion: '2010-03-31' });
		const params = {
			Subject: subject,
			Message: message,
			TopicArn: topicArn,
		};
		sns.publish(params, function (err, data) {
			if (err) {
				return res.json({
					message: 'message not published',
					error: err,
				});
			} else {
				return res.json({
					message: 'message published',
					result: data,
				});
			}
		});
	} catch (err) {
		return res.json({
			message: 'message not published',
			error: err,
		});
	}
});

module.exports = router;
