FROM python:3.9.19

WORKDIR /app

COPY requirements.txt .
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
# RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .
WORKDIR /app
ENV PYTHONUNBUFFERED=1
# RUN groupadd -g 1000 app_group

# RUN useradd -g app_group --uid 1000 app_user

# RUN chown -R app_user:app_group /app

# USER app_user

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]