









from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from opencode_bridge import send_to_opencode


class RequestHandler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/":
            self.send_json(200, {
                "status": "ok",
                "message": "Our AI Broker is running"
            })
        else:
            self.send_json(404, {
                "error": "Not found"
            })

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_json(404, {
                "error": "Not found"
            })
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))

            prompt = data.get("prompt", "").strip()

            if not prompt:
                self.send_json(400, {
                    "error": "Prompt is required"
                })
                return

            response = send_to_opencode(prompt)

            self.send_json(200, {
                "response": response
            })

        except Exception as e:
            self.send_json(500, {
                "error": str(e)
            })


def run():
    server = HTTPServer(("127.0.0.1", 8081), RequestHandler)
    print("Our AI Broker is running on port 8080...")
    server.serve_forever()


if __name__ == "__main__":
    run()
