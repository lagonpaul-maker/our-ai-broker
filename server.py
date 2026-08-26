






























import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from opencode_bridge import send_to_opencode


class RequestHandler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "index.html"
            )

            if not os.path.exists(file_path):
                self.send_json(404, {
                    "error": "index.html not found"
                })
                return

            try:
                with open(file_path, "rb") as f:
                    content = f.read()

                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    "text/html; charset=utf-8"
                )
                self.send_header(
                    "Content-Length",
                    str(len(content))
                )
                self.send_header(
                    "Access-Control-Allow-Origin",
                    "*"
                )
                self.end_headers()
                self.wfile.write(content)

            except Exception as e:
                self.send_json(500, {
                    "error": str(e)
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

            if length <= 0:
                self.send_json(400, {
                    "error": "Request body is required"
                })
                return

            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))

            prompt = data.get("prompt", "").strip()

            if not prompt:
                self.send_json(400, {
                    "error": "Prompt is required"
                })
                return

            print(f"[Broker] Received: {prompt}")

            response = send_to_opencode(prompt)

            self.send_json(200, {
                "response": response
            })

        except json.JSONDecodeError:
            self.send_json(400, {
                "error": "Invalid JSON"
            })

        except Exception as e:
            print(f"[Broker] Error: {e}")
            self.send_json(500, {
                "error": str(e)
            })


def run():
    server = HTTPServer(
        ("127.0.0.1", 8081),
        RequestHandler
    )

    print("======================================")
    print("Our AI Broker")
    print("Website: http://127.0.0.1:8081")
    print("API:     http://127.0.0.1:8081/api/chat")
    print("OpenCode + Ox Alpha: ENABLED")
    print("======================================")

    server.serve_forever()


if __name__ == "__main__":
    run()








