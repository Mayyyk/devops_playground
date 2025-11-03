FROM python:3.10-slim

# To make it identical with local project files
WORKDIR /src_frontend 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# More robust debugging and logging 
ENV PYTHONUNBUFFERED=1 

# Default streamlit port
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]

