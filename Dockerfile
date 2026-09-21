FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md /app/
COPY src /app/src
COPY examples /app/examples
COPY docs /app/docs

RUN pip install --no-cache-dir ".[server]"

EXPOSE 8000
CMD ["uvicorn","aibpe.server:create_app","--host","0.0.0.0","--port","8000"]
