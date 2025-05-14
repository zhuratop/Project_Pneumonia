#!/bin/bash

# Собираем Docker образ
docker build -t pneumonia-app .

# Запускаем контейнер
docker run -d -p 5000:5000 --name pneumonia-container-app pneumonia-app