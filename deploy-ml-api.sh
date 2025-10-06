#!/bin/bash

# Скрипт для деплоя ML-API в продакшене

set -e

echo "🚀 Начинаем деплой ML-API..."

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден! Создайте его перед деплоем."
    echo "Пример содержимого:"
    echo "PETS_DATABASE_PATH=https://storage.yandexcloud.net/pet-match-s3-storage/PetMatch/db.json"
    exit 1
fi

# Останавливаем текущие контейнеры
echo "🛑 Останавливаем текущие контейнеры..."
docker compose -f docker-compose.prod.yaml down || true

# Собираем новый образ
echo "🏗️ Собираем новый образ..."
docker compose -f docker-compose.prod.yaml build --no-cache

# Запускаем новые контейнеры
echo "🚀 Запускаем новые контейнеры..."
docker compose -f docker-compose.prod.yaml up -d

# Ждем запуска сервиса
echo "⏳ Ждем запуска сервиса..."
sleep 10

# Проверяем здоровье сервиса
echo "🔍 Проверяем состояние сервиса..."
if curl -f http://localhost:8001/ > /dev/null 2>&1; then
    echo "✅ ML-API успешно запущен!"
    echo "📊 Статус контейнеров:"
    docker compose -f docker-compose.prod.yaml ps
else
    echo "❌ Ошибка запуска ML-API"
    echo "📋 Логи сервиса:"
    docker compose -f docker-compose.prod.yaml logs ml-api
    exit 1
fi

# Очищаем неиспользуемые образы
echo "🧹 Очищаем неиспользуемые образы..."
docker system prune -f

echo "✅ Деплой ML-API завершен успешно!"
echo "🌐 API доступен по адресу: http://localhost:8001"
