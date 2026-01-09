import http.server as h,urllib.request as u,urllib.error as e,gzip as g,zlib as z
class R(h.BaseHTTPRequestHandler):
 T='https://www.perplexity.ai'
 def do_GET(self):self.p()
 def do_POST(self):self.p()
 def do_HEAD(self):self.p()
 def do_OPTIONS(self):self.p()
 def p(self):
  try:
   d={k:v for k,v in self.headers.items()if k.lower()not in['host','connection','accept-encoding']};d.update({'Host':'www.perplexity.ai','Origin':'https://www.perplexity.ai','Referer':'https://www.perplexity.ai/','Accept-Encoding':'identity'});c=int(self.headers.get('Content-Length',0));b=self.rfile.read(c)if c>0 else None
   with u.urlopen(u.Request(self.T+self.path,data=b,headers=d,method=self.command),timeout=30)as s:
    rb=s.read();ce=s.headers.get('Content-Encoding','').lower()
    if ce=='gzip':
     try:rb=g.decompress(rb)
     except:pass
    elif ce=='deflate':
     try:rb=z.decompress(rb)
     except:pass
    self.send_response(s.status)
    for k,v in s.headers.items():
     if k.lower()not in['transfer-encoding','connection','content-encoding','content-length']:
      if k.lower()=='location'and v.startswith('https://www.perplexity.ai'):v=v.replace('https://www.perplexity.ai','http://localhost:3000')
      self.send_header(k,v)
    self.send_header('Content-Length',len(rb));self.end_headers();self.wfile.write(rb)
  except e.HTTPError as x:self.send_response(x.code);self.end_headers();self.wfile.write(x.read())
  except:pass
 def log_message(self,f,*a):pass
h.HTTPServer(('localhost',3000),R).serve_forever()
