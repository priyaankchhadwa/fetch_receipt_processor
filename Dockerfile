# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /home/app

# Copy requirements.txt first (for better caching)
COPY requirements.txt /home/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application contents
COPY . /home/app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to ensure Python output is sent to terminal
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]