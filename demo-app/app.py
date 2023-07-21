from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, this is a test web application running in Kubernetes!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
