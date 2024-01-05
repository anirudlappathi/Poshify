FROM ubuntu:latest

# Update package lists and install Python3 and pip for Python3
RUN apt-get update && \
    apt-get install -y python3 python3-pip libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install required Python packages using pip3
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

# Specify the command to run your Python application
CMD ["python3", "app.py"]