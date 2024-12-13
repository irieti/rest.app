# Используем Python 3.10 в качестве основы
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip3 install --no-cache-dir -r requirements.txt

# Создаем папки для статики и медиа
RUN mkdir -p /app/staticfiles /app/media

# Копируем все файлы проекта в контейнер
COPY . .

# Собираем статические файлы Django
RUN python3 manage.py collectstatic --noinput

# Открываем порт 8000 для доступа
EXPOSE 8000

# Запускаем сервер Django
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
