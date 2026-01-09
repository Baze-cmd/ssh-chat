#!/usr/bin/env python3
"""
Simple HTTP server to serve the mini.py script for on-demand execution.
Usage: python3 server.py [port]
"""
import http.server
import socketserver
import os
import sys

class ScriptHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.serve_script()
        else:
            self.send_error(404, "Not Found")
    
    def serve_script(self):
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'mini.py')
            with open(script_path, 'r') as f:
                script_content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', len(script_content.encode('utf-8')))
            self.end_headers()
            self.wfile.write(script_content.encode('utf-8'))
            
        except FileNotFoundError:
            self.send_error(500, "mini.py not found")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

if __name__ == '__main__':
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    HOST = '0.0.0.0'
    
    with socketserver.TCPServer((HOST, PORT), ScriptHandler) as httpd:
        print(f"Serving mini.py on http://{HOST}:{PORT}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            httpd.shutdown()
