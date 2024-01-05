FROM alpine:latest

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install Authlib==1.3.0 boto3==1.34.13 Flask==2.2.5 \
    matplotlib==3.8.0 mysql-connector-python==8.1.0 numpy==1.26.0 \
    opencv-python==4.8.1.78 pandas==2.1.1 python-dotenv==1.0.0 \
    scikit-fuzzy==0.4.2 SQLAlchemy==2.0.21 urllib3==1.25.10 \

# Clone the GitHub repository into the Docker image
RUN git clone https://github.com/anirudlappathi/Poshify.git /app

WORKDIR /app

# Define the startup command
CMD ["python3", "Poshify/app.py"]