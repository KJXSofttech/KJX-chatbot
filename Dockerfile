# Use the official Python image as a base image
FROM python:3.12-slim

# Set environment variables to ensure that Python outputs everything to the terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 4000

# Set the entrypoint to run the Flask app
CMD ["python", "app.py"]
