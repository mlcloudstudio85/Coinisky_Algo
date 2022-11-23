const express = require('express');
const axios = require('axios');
const router = express.Router();
const AIRFLOW_URL = process.env.AIRFLOW_URL;
const AIRFLOW_AUTH = process.env.AIRFLOW_AUTH;
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

router.get('/dags', async function (req, res) {
	try {
		const response = await axios.get(`${AIRFLOW_URL}/api/v1/dags`, {
			headers: {
				Authorization: AIRFLOW_AUTH,
			},
		});
		return res.json(response.data);
	} catch (error) {
		return res.status(500).json(error);
	}
});

router.get('/dags/:dag_id', async function (req, res) {
	try {
		const response = await axios.get(
			`${AIRFLOW_URL}/api/v1/dags/${req.params.dag_id}`,
			{
				headers: {
					Authorization: AIRFLOW_AUTH,
				},
			}
		);
		return res.json(response.data);
	} catch (error) {
		return res.status(500).json(error);
	}
});

router.delete('/dags/:dag_id', async function (req, res) {
	try {
		const response = await axios.delete(
			`${AIRFLOW_URL}/api/v1/dags/${req.params.dag_id}`,
			{
				headers: {
					Authorization: AIRFLOW_AUTH,
				},
			}
		);
		return res.json(response.data);
	} catch (error) {
		return res.status(500).json(error);
	}
});

router.get('/dags/:dag_id/tasks', async function (req, res) {
	try {
		const response = await axios.get(
			`${AIRFLOW_URL}/api/v1/dags/${req.params.dag_id}/tasks`,
			{
				headers: {
					Authorization: AIRFLOW_AUTH,
				},
			}
		);

		return res.json(response.data);
	} catch (error) {
		return res.status(500).json(error);
	}
});

router.get('/dags/:dag_id/dagRuns', async function (req, res) {
	try {
		const response = await axios.get(
			`${AIRFLOW_URL}/api/v1/dags/${req.params.dag_id}/dagRuns`,
			{
				headers: {
					Authorization: AIRFLOW_AUTH,
				},
			}
		);

		return res.json(response.data);
	} catch (error) {
		return res.status(500).json(error);
	}
});

router.post('/dags/:dag_id/dagRuns', async function (req, res) {
	try {
		const { dag_run_id, message } = req.body;
		const response = await axios.post(
			`${AIRFLOW_URL}/api/v1/dags/${req.params.dag_id}/dagRuns`,
			{
				conf: {
					message: message,
				},
				dag_run_id: dag_run_id,
			},
			{
				headers: {
					Authorization: AIRFLOW_AUTH,
				},
			}
		);

		return res.json(response.data);
	} catch (error) {
		return res.status(500).json(error);
	}
});

router.get('/dags/:dag_id/dagRuns/:dag_run_id', async function (req, res) {
	try {
		const response = await axios.get(
			`${AIRFLOW_URL}/api/v1/dags/${req.params.dag_id}/dagRuns/${req.params.dag_run_id}`,
			{
				headers: {
					Authorization: AIRFLOW_AUTH,
				},
			}
		);

		return res.json(response.data);
	} catch (error) {
		return res.status(500).json(error);
	}
});

router.delete('/dags/:dag_id/dagRuns/:dag_run_id', async function (req, res) {
	try {
		const response = await axios.delete(
			`${AIRFLOW_URL}/api/v1/dags/${req.params.dag_id}/dagRuns/${req.params.dag_run_id}`,
			{
				headers: {
					Authorization: AIRFLOW_AUTH,
				},
			}
		);

		return res.json(response.data);
	} catch (error) {
		return res.status(500).json(error);
	}
});

router.patch('/dags/:dag_id/dagRuns/:dag_run_id', async function (req, res) {
	try {
		const response = await axios.patch(
			`${AIRFLOW_URL}/api/v1/dags/${req.params.dag_id}/dagRuns/${req.params.dag_run_id}`,
			{
				state: 'failed',
			},
			{
				headers: {
					Authorization: AIRFLOW_AUTH,
				},
			}
		);

		return res.json(response.data);
	} catch (error) {
		return res.status(500).json(error);
	}
});



module.exports = router;
