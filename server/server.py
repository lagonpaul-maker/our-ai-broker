import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_response(404)
            self.end_headers()
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            user_message = data.get("message", "")
            print(f"Received message: {user_message}")

            # Temporary response.
            # OpenCode integration will replace this later.
            response_data = {
                "message": f"Bridge received: '{user_message}'"
            }

            response = json.dumps(response_data).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        except Exception as e:
            error = json.dumps({"message": f"Server error: {e}"}).encode("utf-8")

            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(error)))
            self.end_headers()
            self.wfile.write(error)


def run():
    # Listen on all interfaces so the Android-to-Termux connection
    # can be configured properly later.
    server_address = ("0.0.0.0", 8080)

    httpd = HTTPServer(server_address, RequestHandler)

    print("Starting Our AI Broker bridge on port 8080...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
