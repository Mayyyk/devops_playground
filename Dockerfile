# BUILDER

FROM python:3.10-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# FINAL

FROM python:3.10-slim-bullseye

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3:.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY app.py .

ENV PYTHONBUFFERED=1

EXPOSE 5000

CMD ["python", 'app.py']