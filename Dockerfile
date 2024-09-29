# Use official Python image
FROM python:3.12-slim

# Install environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create work directory
WORKDIR /app

# Install system depends
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
#RUN  apt-get update && apt-get install -y \
#    libpq-dev python-dev-is-python3

#COPY config/requirements/requirements.txt /app/

COPY config/requirements/requirements.txt /app/

RUN pip install -r requirements.txt

# Copy the project to the work directory
COPY . /app/


# Команда для запуска Gunicorn
CMD ["./entry_point.sh"]
