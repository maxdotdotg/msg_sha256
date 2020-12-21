from http.server import BaseHTTPRequestHandler
from messages import fetch_message, write_message, delete_message
import logging


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        route = self.path.split("/")[1].strip("/")
        if route == "messages":
            logging.info("hit messages")
            query = fetch_message(self.path.split("/")[2])
            message = query["response"]
            status = query["status"]
        elif route == "metrics":
            logging.info("hit metrics")
            message = "hit /metrics"
            status = 200
        elif route == "":
            message = "hit the root"
            status = 200
        else:
            message = f"not found, yo. path was {self.path} and route was {route}"
            status = 404

        self.respond(status, message)

    def do_POST(self):
        route = self.path.split("/")[1].strip("/")
        print("route is:", route)
        if route == "messages":
            try:
                length = int(self.headers["Content-Length"])
                content = str(self.rfile.read(length)).strip("b'")
                print(f"message body exists: {content}")
                message = content
                status = 9001
            except TypeError:
                print("caught type error")
                message = "body must be in the form of { 'message': 'hello there' }"
                status = 405
        else:
            message = f"not found, yo. path was {self.path} and route was {route}"
            status = 404

    def handle_http(self, status, message, content_type):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        return bytes(str(message), "UTF-8")

    def respond(self, status, message):
        content = self.handle_http(status, message, "application/json")
        self.wfile.write(content)
