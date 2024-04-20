from json import dumps
from flask import Flask, send_from_directory
import os

from www.cv import SERVER_IP

app = Flask(__name__)

# Route to serve static files (CSS, JS, images)
@app.route('/<path:path>')
def serve_static(path):
    if path == 'index.json':
        return dumps(list(filter(lambda filename: not filename.endswith('.html') and not filename.endswith('.js'), os.listdir('www'))))
    return send_from_directory('www', path)

# Route to serve the index.html template
@app.route('/')
def index():
    return send_from_directory('www', 'index.html')

if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname) 
    app.run(host=SERVER_IP, port=5000)
