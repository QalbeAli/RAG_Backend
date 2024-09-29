# Use an official Python image as the base image
FROM python:3.10-slim

# Set the working directory inside the container (the root of the project)
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock first to leverage Docker cache
COPY pyproject.toml poetry.lock /app/

# Install the dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the rest of the project files
COPY . /app/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Set environment variables (if needed, adjust according to your .env file)
# ENV VAR_NAME=value

# Command to run the FastAPI application
CMD ["poetry", "run", "uvicorn", "hospital_rag:app", "--host", "0.0.0.0", "--port", "8000"]
