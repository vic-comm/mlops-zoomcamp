# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency file first to cache the installation step
COPY requirements.txt .

# Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code (app.py, model files, etc.)
COPY . .

# expose the port your app runs on
EXPOSE 9696

# The command to start your application
CMD ["python", "app.py"]