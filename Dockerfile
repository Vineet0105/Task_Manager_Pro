# 1) Use an official lightweight Python image
FROM python:3.11-slim

# 2) Set working directory inside container
WORKDIR /app

# 3) Copy only requirements first (to leverage Docker caching)
COPY requirements.txt /app/

# 4) Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copy all project files into container
COPY . /app/

# 6) Expose port Django will run on
EXPOSE 8000

# 7) Default command for Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
