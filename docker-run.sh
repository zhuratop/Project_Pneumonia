#!/bin/bash

# Собираем Docker образ
docker build -t pneumonia-detector .

# Запускаем контейнер
docker run -d \
    --name pneumonia-detector \
    -p 5000:5000 \
    -v "$(pwd)/uploads:/app/uploads" \
    -v "$(pwd)/pneumonia.db:/app/pneumonia.db" \
    pneumonia-detector 