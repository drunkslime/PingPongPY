import http.server
import socketserver
import webbrowser
import threading
import os
import subprocess

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/start':
            #Execute the game script
            subprocess.Popen(['python', 'main.py'])
            self.send_response(200)
            self.end_headers()
        else:
            #Serve index.html by default
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
#Server index.html on localhost:8000
with socketserver.TCPServer(('', 8000), Handler) as httpd:
    print('Server started at http://localhost:8000')
    #Open the web browser
    webbrowser.open_new_tab("http://localhost:8000")
    #Start the server
    httpd.serve_forever()