FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

COPY app app

ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5566

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5566"]