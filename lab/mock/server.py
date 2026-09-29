#!/usr/bin/env python3
"""Loopback Databricks HTTP mock. Logs every request path; secrets/get returns the witness."""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

WITNESS = "N8N-DBX-SECRET-WITNESS"
SECRET_PATH = "/api/2.0/secrets/get"
LOG_LOCK = threading.Lock()
ACCESS_LOG: list[str] = []


def record(line: str) -> None:
    with LOG_LOCK:
        ACCESS_LOG.append(line)
        print(line, flush=True)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args: object) -> None:
        return

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, payload: object) -> None:
        raw = json.dumps(payload, separators=(",", ":")).encode()
        self._send(code, raw, "application/json")

    def _handle(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parsed.query
        line = f"{self.command} {self.path}"
        if path not in ("/health", "/__logs"):
            record(line)

        if path in ("/health", "/healthz"):
            self._send(200, b"ok", "text/plain")
            return

        if path == "/__logs":
            with LOG_LOCK:
                body = ("\n".join(ACCESS_LOG) + ("\n" if ACCESS_LOG else "")).encode()
            self._send(200, body, "text/plain; charset=utf-8")
            return

        if self.command == "GET" and path.rstrip("/") == SECRET_PATH:
            self._json(200, {"value": WITNESS, "scope": "s", "key": "k", "query": qs})
            return

        self._json(
            404,
            {
                "error_code": "NOT_FOUND",
                "message": f"no mock handler for {self.command} {path}",
            },
        )

    def do_GET(self) -> None:  # noqa: N802
        self._handle()

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)
        self._handle()

    def do_PUT(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)
        self._handle()

    def do_HEAD(self) -> None:  # noqa: N802
        self._handle()


if __name__ == "__main__":
    httpd = ThreadingHTTPServer(("0.0.0.0", 8080), Handler)
    httpd.serve_forever()
