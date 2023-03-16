FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Expose the port used by the application
EXPOSE 8080

# Set the entrypoint command for the container
CMD ["python", "main.py"]
