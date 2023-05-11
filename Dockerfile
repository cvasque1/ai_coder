# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /prelim

# Install dependencies
COPY requirements.txt /prelim/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /prelim/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 prelim.wsgi:application

