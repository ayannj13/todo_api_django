FROM python:3.11-slim

# Faster Python in containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps inside the image
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project into the image
COPY . .

EXPOSE 8000

# Run migrations and start the dev server
CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
