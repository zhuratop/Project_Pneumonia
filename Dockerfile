# Используем Ubuntu 22.04 как базовый образ
FROM ubuntu:22.04

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Europe/Moscow

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Копируем файлы приложения
COPY . .

# Создаем директорию для загрузок
RUN mkdir -p uploads

# Открываем порт
EXPOSE 5000

# Запускаем приложение
CMD ["python3", "app.py"] 