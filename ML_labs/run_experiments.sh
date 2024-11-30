#!/bin/bash

# Строим Docker-образ
docker build -t ml-experiment .

# Запускаем контейнер с MLFlow
docker run -e AWS_ACCESS_KEY_ID=your_access_key -e AWS_SECRET_ACCESS_KEY=your_secret_key -p 5000:5000 ml-experiment
