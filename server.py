from http.server import BaseHTTPRequestHandler
from messages import fetch_message, write_message, delete_message
from metrics import get_metrics
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
                content = literal_eval(self.rfile.read(length).decode("UTF-8"))

                print("calling write_message with", content["message"])
                query = write_message(content["message"])
                message = query["response"]
                status = query["status"]
            except TypeError as e:
                print("caught type error:", e)
                message = "body must be in the form of { 'message': 'hello there' }"
                status = 405
        else:
            message = f"not found, yo. path was {self.path} and route was {route}"
            status = 404

        self.respond(status, message)

    def do_DELETE(self):
        route = self.path.split("/")[1].strip("/")
        if route == "messages":
            query = delete_message(self.path.split("/")[2])
            message = query["response"]
            status = query["status"]
        else:
            message = f"not found, yo. path was {self.path} and route was {route}"
            status = 404

        self.respond(status, message)


    def do_PUT(self):
        message = "Not Allowed"
        status = 405
        self.respond(status, message)

    def do_HEAD(self):
        message = "Not Allowed"
        status = 405
        self.respond(status, message)

    def handle_http(self, status, message, content_type):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()

        # incremenmt request qty?
        return bytes(str(message), "UTF-8")

    def respond(self, status, message):
        content = self.handle_http(status, message, "application/json")
        self.wfile.write(content)
