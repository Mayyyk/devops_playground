import streamlit as st
import requests
import pandas as pd
import os

# 1. Get the URL of our backend (API) from an environment variable
# We set a default URL to localhost for easier testing outside of Docker
API_BASE_URL = os.environ.get("API_URL", "http://127.0.0.1:5000") # second argument is a backup if API_URL set in docker-compose is not found
STEP_RESPONSE_URL = f"{API_BASE_URL}/api/step_response"

st.set_page_config(layout="wide")
st.title("Dynamic Object Simulator 📈")

st.sidebar.header("About the Simulator")
st.sidebar.info(
    "This application visualizes the step response of a first-order object "
    "(e.g., a water tank), which is simulated by a separate backend API."
)

@st.cache_data(ttl=60) # Cache data for 60 seconds
def get_simulation_data():
    """Fetches data from our Flask API."""
    try:
        response = requests.get(STEP_RESPONSE_URL)
        response.raise_for_status() # Raise an error if the API returned an error
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to the API at: {STEP_RESPONSE_URL}")
        return None
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return None

data = get_simulation_data()

if data:
    st.header("Step Response")
    
    # Prepare data for the chart
    sim_data = data.get("simulation", {})
    df = pd.DataFrame({
        "Time (s)": sim_data.get("time_s", []),
        "Temperature": sim_data.get("temperature", [])
    })
    
    st.line_chart(df.set_index("Time (s)"))
    
    st.header("Model Parameters")
    model_data = data.get("model", {})
    col1, col2 = st.columns(2)
    col1.metric("Gain (K)", model_data.get("K", "N/A"))
    col2.metric("Time Constant (tau)", f"{model_data.get('tau', 'N/A')} s")
    
    st.subheader("Transfer Function")
    st.code(model_data.get("tf", "N/A"), language="text")
    
    st.header("Raw JSON Data")
    st.json(data)
