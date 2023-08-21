# Pull official base image
FROM python:3.8-slim

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

# Create directories for logs
RUN touch /var/log/filebeat.log /var/log/filebeat.log.1 && \
    chmod 664 /var/log/filebeat.log /var/log/filebeat.log.1

# Install dependencies
COPY Pipfile.lock Pipfile ./


RUN pip install --no-cache-dir -U setuptools pip pipenv \
    && CI=1 pipenv install --dev --deploy --system \
    && pipenv --clear

# Copy project files
COPY . .

# Make entrypoint.sh executable
RUN chmod +x ./entrypoint.sh

# Publish network port
EXPOSE 5000

# Execute script to start the application web server
ENTRYPOINT ["./entrypoint.sh"]
