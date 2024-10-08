# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt || \
    pip install langchain-community==0.0.1 || \
    (echo "Failed to install packages. Check your requirements.txt file." && exit 1)

# Download spaCy model
RUN python -m spacy download en_core_web_sm || \
    (echo "Failed to download spaCy model. Check your internet connection." && exit 1)

# Copy the current directory contents into the container at /app
COPY . .

# Remove unnecessary files to reduce image size
RUN find . -type d -name __pycache__ -exec rm -rf {} + && \
    rm -rf ~/.cache/pip

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME=World

# Run main.py when the container launches
CMD ["python", "main.py"]