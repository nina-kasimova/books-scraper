# Use official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your project
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run FastAPI when the container starts
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0","--reload"]

