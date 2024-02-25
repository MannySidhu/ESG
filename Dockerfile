# Use a lightweight Python base image
FROM python:3.8-slim

# Install system dependencies required for certain Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch transformers boto3 codecarbon flask

# Create a directory for emissions data and adjust permissions
RUN mkdir /emissions_data && chmod 777 /emissions_data

# Set environment variables for SageMaker (if using)
ENV SAGEMAKER_SUBMIT_DIRECTORY /opt/ml/model/code
ENV SAGEMAKER_PROGRAM inference_script.py

# Copy the application and script to the container
COPY . /opt/ml/model/code

# Set the working directory
WORKDIR /opt/ml/model/code

# Specify a non-root user for increased security
#RUN useradd appuser
#USER appuser

# Define the entrypoint to run the Flask application
ENTRYPOINT ["python", "inference_script.py"]

# Optional health check (comment out if not needed)
#CMD ["bash", "-c", "while true; do echo '[OK]' && sleep 30; done"]

# Expose port 8080 for the Flask application
EXPOSE 8080
