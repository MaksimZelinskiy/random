FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY src/bot/requirements.txt /app/
RUN pip install -r requirements.txt

# Copy bot directory and required fast_api components
COPY src/bot/ /app/
COPY database/ /app/database    
COPY utils_system/ /app/utils_system

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Run from the correct directory
CMD ["python", "app_polling.py"]
