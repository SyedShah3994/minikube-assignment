from flask import Flask
import os, socket

app = Flask(__name__)

@app.route('/')
def home():
    pod = os.environ.get('POD_NAME', socket.gethostname())
    return f'<h1>Hello from pod: {pod}</h1>\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)