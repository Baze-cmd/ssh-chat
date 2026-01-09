import http.server
import urllib.request
import urllib.error
import gzip
import zlib

class ReverseProxyHandler(http.server.BaseHTTPRequestHandler):
    TARGET = 'https://www.perplexity.ai'
    
    def do_GET(self):
        self.proxy_request()
    
    def do_POST(self):
        self.proxy_request()
    
    def do_HEAD(self):
        self.proxy_request()
    
    def do_OPTIONS(self):
        self.proxy_request()
    
    def proxy_request(self):
        try:
            # Build target URL
            target_url = self.TARGET + self.path
            
            # Copy headers from incoming request
            headers = {}
            for header, value in self.headers.items():
                if header.lower() not in ['host', 'connection', 'accept-encoding']:
                    headers[header] = value
            headers['Host'] = 'www.perplexity.ai'
            headers['Origin'] = 'https://www.perplexity.ai'
            headers['Referer'] = 'https://www.perplexity.ai/'
            # Don't request compressed content
            headers['Accept-Encoding'] = 'identity'
            
            # Read body for POST requests
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Create and send request
            req = urllib.request.Request(
                target_url,
                data=body,
                headers=headers,
                method=self.command
            )
            
            # Get response
            with urllib.request.urlopen(req, timeout=30) as response:
                # Read the response body
                response_body = response.read()
                
                # Try to decompress if needed
                content_encoding = response.headers.get('Content-Encoding', '').lower()
                if content_encoding == 'gzip':
                    try:
                        response_body = gzip.decompress(response_body)
                    except:
                        pass
                elif content_encoding == 'deflate':
                    try:
                        response_body = zlib.decompress(response_body)
                    except:
                        pass
                
                # Send status
                self.send_response(response.status)
                
                # Send headers (skip encoding-related headers)
                for header, value in response.headers.items():
                    if header.lower() not in ['transfer-encoding', 'connection', 'content-encoding', 'content-length']:
                        if header.lower() == 'location' and value.startswith('https://www.perplexity.ai'):
                            value = value.replace('https://www.perplexity.ai', 'http://localhost:3000')
                        self.send_header(header, value)
                
                # Send correct content length
                self.send_header('Content-Length', len(response_body))
                self.end_headers()
                
                # Send body
                self.wfile.write(response_body)
                
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            try:
                self.wfile.write(e.read())
            except:
                pass
        except BrokenPipeError:
            pass
        except Exception as e:
            print(f"Error: {e}")
            try:
                self.send_response(502)
                self.end_headers()
                self.wfile.write(b'Bad Gateway')
            except:
                pass
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

if __name__ == '__main__':
    PORT = 3000
    print(f'Reverse proxy running on http://localhost:{PORT}')
    print(f'Proxying all requests to https://www.perplexity.ai')
    print('Press Ctrl+C to stop')
    
    server = http.server.HTTPServer(('localhost', PORT), ReverseProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down...')
        server.shutdown()
