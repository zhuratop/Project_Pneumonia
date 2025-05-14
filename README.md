# Pneumonia Detection App

Приложение для определения пневмонии по рентгеновским снимкам с использованием глубокого обучения.

## Запуск через Docker

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/pneumonia-detection.git
cd pneumonia-detection
```

2. Запустите приложение с помощью Docker:
```bash
./docker-run.sh
```

После запуска приложение будет доступно по адресу: http://localhost:5000

## Структура проекта

- `app.py` - основной файл приложения
- `models/` - директория для хранения модели
- `uploads/` - директория для временного хранения загруженных изображений
- `templates/` - HTML шаблоны
- `static/` - статические файлы (CSS, JavaScript)
- `pneumonia.db` - база данных SQLite для хранения результатов

## Технологии

- Python 3.11
- Flask
- TensorFlow
- SQLite
- Docker 