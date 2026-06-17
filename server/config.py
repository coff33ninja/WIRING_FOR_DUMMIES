"""Configuration — port, paths, MIME types, network IP."""

import os
import socket
import sys
from pathlib import Path

# Project root is one level above server/
DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000

MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css",
    ".js": "application/javascript",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}


def self_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"
    finally:
        s.close()
