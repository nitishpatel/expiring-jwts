# Use official Python image
FROM python:3.13

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Configure Poetry to install dependencies system-wide
RUN poetry config virtualenvs.create false

# Copy the entire application first
COPY . .

# Ensure the project directory contains pyproject.toml
RUN ls -la /app

# Install dependencies
RUN poetry install --no-root

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["poetry", "run", "devrun"]
