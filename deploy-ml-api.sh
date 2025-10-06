#!/bin/bash

# Скрипт для деплоя ML-API в продакшене

set -e

echo "🚀 Начинаем деплой ML-API..."

# Генерируем .env файл если есть переменные окружения
if [ -n "$PETS_DATABASE_PATH" ]; then
    echo "🔧 Генерируем .env файл из переменных окружения..."
    ./generate-env.sh
elif [ ! -f .env ]; then
    echo "❌ Файл .env не найден и переменные окружения не установлены!"
    echo "Создайте .env файл или установите переменные окружения."
    echo "Пример содержимого:"
    echo "PETS_DATABASE_PATH=https://storage.yandexcloud.net/pet-match-s3-storage/PetMatch/db.json"
    exit 1
else
    echo "✅ Используем существующий .env файл"
fi

# Создаем общую сеть если её нет
echo "🌐 Проверяем общую сеть..."
if ! docker network ls | grep -q petmatch-network; then
    echo "🌐 Создаем общую сеть petmatch-network..."
    docker network create petmatch-network
    echo "✅ Сеть petmatch-network создана"
else
    echo "✅ Сеть petmatch-network уже существует"
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
