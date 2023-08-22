# Pull official base image
FROM python:3.8-slim

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

# Install dependencies
COPY Pipfile.lock Pipfile ./
RUN pip install --no-cache-dir -U setuptools pip pipenv \
    && CI=1 pipenv install --dev --deploy --system \
    && pipenv --clear

# Copy project files
COPY . .

# Run db init and update loop
CMD ["python", "-u", "main.py"]
