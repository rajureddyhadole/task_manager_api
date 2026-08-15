# 1. Use a lightweight Python image
FROM python:3.12-slim

# 2. Prevent Python from buffering console logs
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your Django project code
COPY . .
RUN python manage.py collectstatic --noinput

# 6. Expose the port Django runs on
EXPOSE 8000

# 7. Start the Django development server
CMD ["gunicorn", "task_manager.wsgi:application", "--bind", "0.0.0.0:8000"]
