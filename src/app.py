from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Kocham Cię słoneczko ty moje piękne kochane" # I love you Karolcia


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    