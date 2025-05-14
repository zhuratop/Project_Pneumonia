#!/bin/bash

# Собираем Docker образ
docker build -t pneumonia-app .

# Запускаем контейнер
docker run -d --name pneumonia-container-app pneumonia-app git