# Use Python 3.12 slim as the base image
FROM python:3.12.0-slim-bookworm

# Set environment variables to improve Python performance
ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1

# Define application directory
ENV APP=/app

# Set the working directory
WORKDIR $APP

# Copy the requirements.txt file
COPY requirements.txt $APP/

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . $APP/

# Expose the application port
EXPOSE 8000

# Ensure entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
