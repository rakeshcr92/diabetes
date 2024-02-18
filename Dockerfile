# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages including scikit-learn
RUN pip install Flask joblib scikit-learn

# Expose the port the app runs on
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "app.py"]
