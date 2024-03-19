from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
import re
from http.cookies import SimpleCookie
import uuid
import redis
import os
from bs4 import BeautifulSoup

r = redis.Redis(host='localhost', port=6379, db=0)

# Código basado en:
# https://realpython.com/python-http-server/
# https://docs.python.org/3/library/http.server.html
# https://docs.python.org/3/library/http.cookies.html
mappings =[
    (r"^/books/(?P<book_id>\d+)$", "get_book"),
    (r"^/$", "index"),
    ]


class WebRequestHandler(BaseHTTPRequestHandler):
    
    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))
    
    def get_session(self):
        cookies = self.cookies
        session_id = None
        if not cookies:
            session_id = uuid.uuid4()
            
        else:
            session_id = cookies["session_id"].value
        
        return session_id
    
    def write_session_cookie(self,session_id):
        cookies = SimpleCookie()
        cookies["session_id"]=session_id
        cookies["session_id"]["max-age"]=1000
        self.send_header("Set-Cookie", cookies.output(header=""))
    
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    def get_params(self, pattern, path):
        match=re.match(pattern, path)
        if match:
          return match.groupdict()
        else:
          return None

    
    def url_mapping_response(self):
        for pattern, method in mappings:
            match = self.get_params(pattern, self.path)
            print(match)
            if match is not None:
                md = getattr(self, method)
                md(**match)
                return
        
        self.send_response(404)
        self.end_headers()
        self.wfile.write("Not Found".encode("utf-8"))
        
    def index(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        index_page = "<h1> Bienvenidos a los libros </h1>".encode("utf-8")
        
        self.wfile.write(index_page)
        self.load_folder('html/books/')
        
    def get_book(self,book_id):
        session_id =self.get_session()
        r.lpush(f"session:{session_id}", f"book:{book_id}")
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.write_session_cookie(session_id)
        self.end_headers()
        book_info = r.get(f"book:{book_id}") or "<h1> No existe el libro </h1>"
        self.wfile.write(str(book_info).encode("utf-8"))
        self.wfile.write(f"Session Id:{session_id}".encode("utf-8"))
        
        book_list = r.lrange(f"Session Id:{session_id}",0,-1)
        for book in book_list:
            self.wfile.write(f"book:{book}".encode("utf-8"))
        
    
        
    def create_index(self,book_id, html):
        soup = BeautifulSoup(html, 'html.parser')
        texto = soup.get_text()
        lista_texto = texto.split(' ')
        for t in lista_texto:
            r.sadd(t, book_id)

       
        
    def do_GET(self):
       self.url_mapping_response()
    
    
    
    def load_folder(self,path):
        files = os.listdir(path)
        print(files)
        for file in files:
            match = re.match(r'^book(\d+).html$', file)
            if match:
                with open(path + file) as f:
                    html = f.read()
                    book_id = match.group(1)              
                    r.set(book_id, html)
                    self.create_index(book_id, html)
                    print(match.group(0), book_id)  
       
       
             
    def get_response(self):
        return f"""
    <h1> Hola Web </h1>
    <p>  {self.path}         </p>
    <p>  {self.headers}      </p>
    <p>  {self.cookies}      </p>
    <p>  {self.query_data}   </p>

"""
if __name__ == "__main__":
    print("Server starting...")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
