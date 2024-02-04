# Dockerfile for Django application

# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=ml_training_hub.settings

# Run app.py when the container launches
CMD ["gunicorn", "ml_training_hub.wsgi:application", "--bind", "0.0.0.0:8000"]