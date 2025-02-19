# Use official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
