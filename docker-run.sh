#!/bin/bash

# Собираем Docker образ
docker build -t pneumonia-detector .

# Запускаем контейнер
docker run -d --name pneumonia-detector \
    -p 5000:5000 \
    -e TF_ENABLE_ONEDNN_OPTS=0 \
    -v "$(pwd)/uploads:/app/uploads" \
    -v "$(pwd)/pneumonia.db:/app/pneumonia.db" \
    pneumonia-detector 