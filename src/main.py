# Main simulation file
'''
K - gain

tau - T - time constant - how fast temperature is growing, time to gain ~63% of temperature change

Model: G(s) = K / (tau*s + 1)

'''

import numpy as np
import control as ct

K = 20 # Temp rise by 20 degrees
tau = 120 # in seconds

tank_model = ct.tf([K], [tau, 1])

T_SIM = tau * 5 # Simulation duration time set to 5 time constants
N_POINTS = 1000

time_vector = np.linspace(0, T_SIM, N_POINTS)

def get_step_response():
    print("Running step response simulation...")
    
    t_out, y_out = ct.step_response(tank_model, time_vector)
    
    response_data = {
        "model": {
            "K": K,
            "tau": tau,
            "tf": str(tank_model).strip()
        },
        "simulation": {
            "time_s": list(t_out),
            "temperature": list(y_out)
        
        }
    }
    
    print("Simulation finished. Returning data...")
    
    return response_data

print(get_step_response())