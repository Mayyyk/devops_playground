from flask import Flask, jsonify
from main import get_step_response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Default / route"

@app.route('/api/step_response')
def api_step_response():
    print("Got /api/step_response request")
    data_dict = get_step_response()
    print("Returning data...")
    return jsonify(data_dict)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    