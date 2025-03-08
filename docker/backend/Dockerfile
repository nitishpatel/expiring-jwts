# Use official Python image
FROM python:3.13

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Configure Poetry to install dependencies system-wide
RUN poetry config virtualenvs.create false

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy the application files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["poetry","run","devrun"]
