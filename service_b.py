import os

from http.server import BaseHTTPRequestHandler, HTTPServer

import service_a_client
from service_a_client.rest import ApiException


SERVICE_A_URL = os.environ.get(
    "SERVICE_A_URL",
    "http://10.62.104.250:8001"
)

configuration = service_a_client.Configuration(host=SERVICE_A_URL.rstrip("/"))


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path != "/ping":
            self.send_response(404)
            self.end_headers()
            return

        try:
            with service_a_client.ApiClient(configuration) as api_client:
                people = service_a_client.DefaultApi(api_client).get_people(
                    _request_timeout=5
                )

            text = " | ".join(f"{p.name}, {p.addr}" for p in people)
            status = 200

        except (ApiException, OSError, ValueError):
            text = "ServiceA ist nicht erreichbar oder liefert ungueltige Daten."
            status = 502

        body = text.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":

    print("ServiceB laeuft auf http://localhost:8002/ping", flush=True)

    HTTPServer(("0.0.0.0", 8002), Handler).serve_forever()