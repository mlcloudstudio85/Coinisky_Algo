const generateKey = (fileName) => {
	const key =
		Math.random().toString(36).substring(2, 15) +
		Math.random().toString(36).substring(2, 15);
	return key;
};

module.exports = { generateKey };
