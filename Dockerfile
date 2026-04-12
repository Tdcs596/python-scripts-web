FROM python:3.11-slim

# install system dependency
RUN apt-get update && apt-get install -y nmap

WORKDIR /app

COPY . /app

# install python libs
RUN pip install --no-cache-dir -r requirements.txt

# run ONLY script2.py
CMD ["python", "script2.py"]
