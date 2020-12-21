from http.server import BaseHTTPRequestHandler

# TODO: handle endpoint checks and 404s with a function because DRY


class Server(BaseHTTPRequestHandler):

    def do_DELETE(self):
        route = self.path.split("/")[0]
        if route == "messages":
            delete_message(self.path.split("/")[1])
        else:
            content_type = "application/json"
            status = 404


    def do_GET(self):
        route = self.path.split("/")[0]
        if route == "messages":
            fetch_message(self.path.split("/")[1])
        elif route == "metrics":
            fetch_metrics()
        else:
            content_type = "application/json"
            status = 404

    def do_POST(self):
        route = self.path.split("/")[0]
        if route == "messages":
            write_message(self.path.split("/")[1])
        else:
            content_type = "application/json"
            status = 404

    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

        # wtf even is this, still gotta work out how to pass content back
        route_content = routes[self.path]
        return bytes(route_content, "UTF-8")
    
    def respond(self):
        content = self.handle_http(200, "text/html")
        self.wfile.write(content)

