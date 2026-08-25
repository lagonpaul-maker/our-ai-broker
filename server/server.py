import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from opencode_bridge import send_to_opencode


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
            user_message = data.get("message", "").strip()

            if not user_message:
                raise ValueError("Message cannot be empty.")

            print(f"Received message: {user_message}")

            opencode_reply = send_to_opencode(user_message)

            response_data = {
                "message": opencode_reply
            }
            status_code = 200

        except Exception as e:
            response_data = {
                "message": f"[Server Error]: {e}"
            }
            status_code = 500

        response = json.dumps(response_data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


def run():
    # Listen on all interfaces so Android can reach the bridge.
    server_address = ("0.0.0.0", 8080)

    httpd = HTTPServer(server_address, RequestHandler)

    print("Starting Our AI Broker bridge on port 8080...")
    print("OpenCode integration enabled.")

    httpd.serve_forever()


if __name__ == "__main__":
    run()
