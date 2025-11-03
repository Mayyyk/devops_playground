# BUILDER

FROM python:3.10-slim 

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py main.py /src/

# More robust debugging and logging 
ENV PYTHONUNBUFFERED=1 

EXPOSE 5000

CMD ["python", "app.py"]


# Command to run from root: docker build -t my-app -f src/Dockerfile src/