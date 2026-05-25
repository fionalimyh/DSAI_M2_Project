#!/usr/bin/env python3
"""
Run the dual-layer delivery time & revenue dashboard
"""
import http.server
import socketserver
import webbrowser
import os
import threading

def start_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    
    with socketserver.TCPServer(("", 8004), Handler) as httpd:
        print("🚀 Delivery Time & Revenue Dashboard running at http://localhost:8004")
        print("📊 URL: http://localhost:8004/brazil_delivery_revenue_dashboard.html")
        print("\n✨ Features:")
        print("   🗺️  Dual-layer map: Delivery time + Revenue overlay")
        print("   🚚 Delivery Time View: Color-coded by delivery speed")
        print("   💰 Revenue View: Size-coded by revenue amount")
        print("   🔄 Dual Layer View: Both metrics simultaneously")
        print("   📈 Correlation analysis between delivery time & revenue")
        print("   🎯 Performance matrix showing business opportunities")
        print("\n⏹️  Press Ctrl+C to stop")
        
        # Auto-open the dashboard
        threading.Timer(1, lambda: webbrowser.open('http://localhost:8004/brazil_delivery_revenue_dashboard.html')).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Server stopped")

if __name__ == "__main__":
    start_server()