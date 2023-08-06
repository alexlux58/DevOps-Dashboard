# Use the official Python image as the base image
# Stage 1: Build Stage
FROM python:3.9 as builder

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Stage
FROM python:3.9-slim

# Copy the Flask application code into the container
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY app app

# Set the environment variable to run Flask in production mode
ENV FLASK_ENV=production

# Expose the port on which the Flask application will run
EXPOSE 5566

# Set the command to run the Flask application
CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5566"]
