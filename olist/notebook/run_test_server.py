#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import threading

PORT = 8005

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    print(f"Test map: http://localhost:{PORT}/test_map_simple.html")
    print(f"Dashboard: http://localhost:{PORT}/brazil_delivery_revenue_dashboard.html")
    threading.Timer(1, lambda: webbrowser.open(f'http://localhost:{PORT}/brazil_delivery_revenue_dashboard.html')).start()
    httpd.serve_forever()
