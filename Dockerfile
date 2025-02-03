# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Expose the application port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "solution:app", "--host", "0.0.0.0", "--port", "8000"]
