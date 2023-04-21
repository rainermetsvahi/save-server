#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import os
import sys
from datetime import datetime

MAX_BODY_LENGTH = 1000 * 1000 * 10 # 10 MB

LISTEN_ADDRESS_PARAM="http-listen-address"
LISTEN_PORT_PARAM="http-listen-port"
DATA_DIR_PARAM="data-dir"

hostName = os.getenv(LISTEN_ADDRESS_PARAM)
serverPort = int(os.getenv(LISTEN_PORT_PARAM))
saveDir = os.getenv(DATA_DIR_PARAM)

if not hostName or not serverPort or not saveDir:
    print("Incomplete conf: %s", os.environ, file=sys.stderr)
    raise Exception("Environment variable %s, %s or %s not set" % \
            (LISTEN_ADDRESS_PARAM, LISTEN_PORT_PARAM, DATA_DIR_PARAM)
    )

saveDir = os.path.abspath(saveDir)
if not os.path.isdir(saveDir):
    raise Exception("The file save directory %s does not exist" % saveDir)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("hello world".encode())
        else:
            self.send_response(404)
        return

    def do_POST(self):
        length = int(self.headers.get('content-length', 0))

        if length > MAX_BODY_LENGTH:
            print("Content-Length too big: ", length, file=sys.stderr)
            self.send_response(400)
        
        print("Received post data(content-length=%d)" % (length), file=sys.stderr)

        body = self.rfile.read(length)
        self.write_to_file(body)

        self.send_response(200)

    def write_to_file(self, contents):
        filename = datetime.now().isoformat("_").replace(":", "")
        full_path = os.path.join(saveDir, filename)

        with open(full_path, "wb") as f:
            f.write(contents)
            f.close()

        print("Wrote %d bytes to file %s" % (len(contents), full_path), file=sys.stderr)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread"""

if __name__ == "__main__":
    webServer = ThreadedHTTPServer((hostName, serverPort), Handler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

