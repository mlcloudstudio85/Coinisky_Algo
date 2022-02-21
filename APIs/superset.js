const express = require('express');
const axios = require('axios');
const AWS = require('aws-sdk');
const router = express.Router();

const supersetCredentials = {
	accessKeyId: process.env.SUPERSET_ACCESS_KEY,
	secretAccessKey: process.env.SUPERSET_SECRET_KEY,
	region: process.env.ATHENA_REGION,
	athenaS3Location: process.env.ATHENA_S3_LOCATION,
};
const awsCredentials = {
	region: process.env.LAMBDA_REGION,
	accessKeyId: process.env.USER_ACCESS_KEY,
	secretAccessKey: process.env.USER_SECRET_KEY,
};
AWS.config.update(awsCredentials);

router.post('/create-user', async function (req, res) {
	try {
		const lambda = new AWS.Lambda();
		const params = {
			FunctionName: 'CreateSupersetUser',
			InvocationType: 'RequestResponse',
			Payload: JSON.stringify(req.body),
		};
		const lambdaResponse = await lambda.invoke(params).promise();
		const lambdaResponseBody = JSON.parse(lambdaResponse.Payload);
		return res.json({
			message: 'user created',
			result: lambdaResponseBody,
		});
	} catch (error) {
		return res.status(500).json(error);
	}
});

router.post('/database-connection', async function (req, res) {
	try {
		const { accessKeyId, secretAccessKey, region, athenaS3Location } =
			supersetCredentials;
		const { database } = req.body;
		const connectionString = `awsathena+rest://${accessKeyId}:${secretAccessKey}@athena.${region}.amazonaws.com/${database}?s3_staging_dir=${athenaS3Location}`;
		return res.status(200).json({
			message: 'database connection successful',
			connectionString,
		});
	} catch (error) {
		return res.status(500).json(error);
	}
});

module.exports = router;
