# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY ./app /app
COPY ./data /data

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK tokenizer model
RUN python -m nltk.downloader punkt

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
