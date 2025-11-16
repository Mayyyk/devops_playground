from simulation.engine import SimulationEngine
from simulation.models import WaterTankModel
from simulation.signals import StepSignal
from simulation.logger import Logger

def get_step_response():
    print("Running step response simulation...")

    # Simulation parameters
    K = 20
    tau = 120
    t_sim = tau * 5
    dt = 1

    # Create components
    model = WaterTankModel(K=K, tau=tau)
    signal = StepSignal(amplitude=1.0)
    logger = Logger()

    # Create and run simulation engine
    engine = SimulationEngine(model=model, signal=signal, logger=logger)
    engine.run_simulation(t_start=0, t_end=t_sim, dt=dt)

    # Get results
    results = logger.get_results()
    
    response_data = {
        "model": {
            "K": K,
            "tau": tau,
            "tf": str(model.model).strip()
        },
        "simulation": results
    }
    
    print("Simulation finished. Returning data...")
    
    return response_data

if __name__ == '__main__':
    print(get_step_response())