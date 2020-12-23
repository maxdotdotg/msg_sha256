from http.server import BaseHTTPRequestHandler
from ast import literal_eval
from json import dumps

from messages import fetch_message, write_message, delete_message
from metrics import get_metrics, record_request


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        route = self.path.split("/")[1].strip("/")
        if route == "messages":
            sha = self.path.split("/")[2]
            if sha != "":
                query = fetch_message(sha)
                message = query["response"]
                status = query["status"]
            else:
                message = "Not Found"
                status = 404
        elif route == "metrics":
            message = get_metrics()
            status = 200
        else:
            message = "Not Found"
            status = 404

        self.respond(status, message)

    def do_POST(self):
        route = self.path.split("/")[1].strip("/")
        if route == "messages":
            try:
                length = int(self.headers["Content-Length"])
                content = literal_eval(self.rfile.read(length).decode("UTF-8"))

                query = write_message(content["message"])
                message = query["response"]
                status = query["status"]
            except TypeError:
                message = "body must be in the form of { 'message': 'hello there' }"
                status = 405
        else:
            message = "Not Found"
            status = 404

        self.respond(status, message)

    def do_DELETE(self):
        route = self.path.split("/")[1].strip("/")
        if route == "messages":
            query = delete_message(self.path.split("/")[2])
            message = query["response"]
            status = query["status"]
        else:
            message = "Not Found"
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

        record_request(self.path)
        return bytes(str(dumps(message)), "UTF-8")

    def respond(self, status, message):
        content = self.handle_http(status, message, "application/json")
        self.wfile.write(content)
