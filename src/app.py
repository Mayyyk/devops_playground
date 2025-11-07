from flask import Flask, jsonify, request
import numpy as np
from models import WaterTankModel
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


@app.route("/api/simulate/step")
def api_simulate_step():
    # Pobierz parametry z URL (np. ?k=20&tau=120)
    k_val = request.args.get('k', default=20, type=float)
    tau_val = request.args.get('tau', default=120, type=float)

    # Twórz obiekt (OOP!)
    tank = WaterTankModel(K=k_val, tau=tau_val)

    # Użyj metod obiektu
    time_vec = np.linspace(0, tau_val * 5, 1000)
    simulation_data = tank.run_step_response(time_vec)

    response = {
        "model": tank.get_params(),
        "simulation": simulation_data
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    