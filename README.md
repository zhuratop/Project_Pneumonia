# Pneumonia Detector

## Установка и запуск на Windows

### Предварительные требования
1. Установленный [Git](https://git-scm.com/download/win)
2. Установленный [Docker Desktop](https://www.docker.com/products/docker-desktop/)
3. Установленный [Python 3.10](https://www.python.org/downloads/) (если хотите запускать без Docker)

### Клонирование проекта
```bash
# Клонируем репозиторий
git clone <URL_вашего_репозитория>
cd <имя_папки_проекта>
```

### Запуск через Docker (рекомендуется)

1. Убедитесь, что Docker Desktop запущен
2. Запустите `docker-start.bat` двойным кликом
3. Приложение будет доступно по адресу: http://localhost:5000
4. Для остановки приложения запустите `docker-stop.bat`

### Запуск без Docker

1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:
```bash
# В PowerShell:
.\venv\Scripts\Activate.ps1
# Или в Command Prompt:
.\venv\Scripts\activate.bat
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите приложение:
```bash
python app.py
```

### Структура проекта
- `app.py` - основной файл приложения
- `requirements.txt` - зависимости Python
- `Dockerfile` - конфигурация Docker
- `docker-start.bat` - скрипт запуска через Docker
- `docker-stop.bat` - скрипт остановки Docker контейнера
- `uploads/` - директория для загруженных файлов
- `pneumonia.db` - база данных приложения

### Примечания
- При первом запуске через Docker будет загружен базовый образ Ubuntu, это может занять некоторое время
- Убедитесь, что порт 5000 не занят другими приложениями
- Для работы с загруженными файлами используйте директорию `uploads/` 