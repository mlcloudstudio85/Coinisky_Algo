const express = require('express');
const axios = require('axios');
const router = express.Router();
const AWS = require('aws-sdk');
const uploadUtils = require('../utils/upload');

// This will setup AWS
AWS.config.update({
	credentials: {
		accessKeyId: process.env.USER_ACCESS_KEY,
		secretAccessKey: process.env.USER_SECRET_KEY,
	},
	bucket: process.env.BUCKET_NAME,
	region: process.env.BUCKET_REGION,
	ContentType: 'application/octet-stream',
});
const s3 = new AWS.S3({
	apiVersion: '2006-03-01',
	signatureVersion: 'v4',
});

// GET - signed url for upload
router.get('/signurl/put/:filename', (req, res) => {
	try {
		const folderId = new Date().toISOString().split('T')[0];
		const userId = 'Jasbir';
		const dir = `${userId}/${folderId}/`;
		const presignedPutUrl = s3.getSignedUrl('putObject', {
			Bucket: process.env.BUCKET_NAME,
			Key: dir + req.params.filename, //filename
			// Expires: 3 * 60 * 60, //time to expire in seconds - 3 hrs
		});
		res.send({ url: presignedPutUrl });
	} catch (error) {
		console.log(error);
		res.status(500).json(error);
	}
});

// GET - signed URL to view
router.get('/signurl/get/:filename', (req, res) => {
	const presignedGetUrl = s3.getSignedUrl('getObject', {
		Bucket: process.env.BUCKET_NAME,
		Key: req.params.filename,
		Expires: 100, //time to expire in seconds - 5 min
	});
	res.send({ url: presignedGetUrl });
});

// GET signed urls for all images in the s3 bucket
router.get('/image', (req, res) => {
	const params = {
		Bucket: process.env.BUCKET_NAME,
	};
	s3.listObjectsV2(params, (err, data) => {
		// Package signed URLs for each to send back to client
		let images = [];
		for (let item of data.Contents) {
			let url = s3.getSignedUrl('getObject', {
				Bucket: process.env.BUCKET_NAME,
				Key: item.Key,
				Expires: 100, //time to expire in seconds - 5 min
			});
			images.push(url);
		}
		res.send(images);
	});
});

router.get('/createMultipartUpload/:filename', async (req, res) => {
	try {
		const folderId = new Date().toISOString().split('T')[0];
		const userId = 'Jasbir';
		const key = uploadUtils.generateKey(req.params.filename);
		const dir = `${userId}/${folderId}/${key}`;
		const params = {
			Bucket: process.env.BUCKET_NAME,
			Key: dir,
			Expires: 100, //time to expire in seconds - 5 min
		};
		s3.createMultipartUpload(params, (err, data) => {
			if (err) {
				console.log(err);
				res.status(500).json(err);
			} else {
				res.send(data);
			}
		});
	} catch (error) {
		console.log(error);
		res.status(500).json(error);
	}
});
router.post('/prepareUploadPart/:filename', async (req, res) => {
	try {
		console.log(req.body);
		const params = {
			Bucket: process.env.BUCKET_NAME,
			Key: req.body.key,
			UploadId: req.body.uploadId,
			PartNumber: req.body.number,
			Body: req.body.body,
		};
		console.log(params);
		s3.uploadPart(params, (err, data) => {
			if (err) {
				console.log(err);
				res.status(500).json(err);
			} else {
				res.send(data);
			}
		});
	} catch (error) {
		console.log(error);
		res.status(500).json(error);
	}
});

module.exports = router;