#!/usr/bin/python3.8
import http.server
import socketserver

PORT = 8000

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("serving as port", PORT)
    httpd.serve_forever()
