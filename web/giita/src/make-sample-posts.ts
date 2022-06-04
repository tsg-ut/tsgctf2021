import {MongoClient} from 'https://deno.land/x/mongo@v0.27.0/mod.ts';
import type {Bson} from 'https://deno.land/x/mongo@v0.27.0/mod.ts';
import {nanoid} from 'https://deno.land/x/nanoid@v3.0.0/mod.ts'

const client = new MongoClient();
await client.connect('mongodb://mongo:27017');

const mongo = client.database('giita');

export interface PostSchema {
	_id: Bson.ObjectId,
	id: string,
	body: string,
	title: string,
	theme: string,
	isSample: boolean,
}

const Posts = mongo.collection<PostSchema>('posts');

await Posts.deleteMany({isSample: true});

await Posts.insertOne({
	id: nanoid(),
	body: `
		<h1>Welcome to Giita!</h1>
		<img src="https://i.imgur.com/QcT2B3l.png" alt="Giita">
		<p>Giita is a social knowledge sharing for software engineers. Let's share your knowledge or ideas to the world.</p>
		<h2>Features</h2>
		<h3>Amazingly fast loading</h3>
		<p>Simplicity is the most important thing. By eliminating useless functions and advertisements, we have succeeded in achieving the most optimized page loading time possible. There is no need for a "like" button or comments when all you want to do is read the text. When you think of something, you can write it right away and you can read them immediately. This is our motto and the first user experience we want to deliver to you.</p>
		<h3>Fully compatible with HTML</h3>
		<p>The sky is the limit; you can use all the syntax of HTML.</p>
		<p>Have you ever struggled with Markdown because it is so inflexible? As is well known, outdated technologies are often easier to use. By adopting HTML for article formatting, we support all of the rich markup supported by browsers and the writing of semantically sound documents. No more hassling with incorrectly recognized indentations for bullets!</p>
		<h3>First-class security</h3>
		<p>Website without security is good-for-nothing. We employ the most advanced security engineers in the world and always use the latest technology to protect your data. In addition to the basic security measures and penetration tests, we also use the most advanced technologies such as DOMPurify and CSP to provide you with absolute peace of mind.</p>
	`,
	title: 'Welcome to Giita! - How to use it?',
	theme: 'base16.solarized.dark',
	isSample: true,
});

await Posts.insertOne({
	id: nanoid(),
	body: `
		<h1>Basics of SQL injection!</h1>
		<p>SQL injection is a web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database.</p>
		<h2>Example:</h2>
		<pre><code>https://example.com/users?id=1%20UNION%20SELECT%20IF(SUBSTRING(user_password%2C%201%2C%201)%20%3D%20CHAR(50)%2C%20BENCHMARK(5000000%2C%20ENCODE('MSG'%2C%20'by%205%20seconds'))%2C%20null)%20FROM%20users%20WHERE%20user_id%20%3D%201</code></pre>
		<p>becomes...</p>
		<pre><code class="language-javascript">SELECT id, title, body
FROM items
WHERE id = 1 UNION SELECT IF(SUBSTRING(user_password, 1, 1) = CHAR(50), BENCHMARK(5000000, ENCODE('MSG', 'by 5 seconds')), null) FROM users WHERE user_id = 1;</code></pre>
	`,
	title: 'Basics of SQL injection',
	theme: 'base16.monokai',
	isSample: true,
});
