#!/bin/bash

# Скрипт для генерации .env файла из переменных окружения
# Используется в CI/CD для автоматического создания конфигурации ML-API

set -e

ENV_FILE=".env"

echo "🔧 Генерируем .env файл для ML-API..."

# Проверяем обязательные переменные
required_vars=(
    "PETS_DATABASE_PATH"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Ошибка: переменная $var не установлена"
        exit 1
    fi
done

# Создаем .env файл
cat > "$ENV_FILE" << EOF
# ML-API Configuration
# Generated at: $(date)

# Database Configuration (S3 Storage)
PETS_DATABASE_PATH=${PETS_DATABASE_PATH}

# API Configuration
API_URL=${API_URL:-http://localhost:8001}

# Optional: Bot Configuration (if using Telegram bot)
BOT_TOKEN=${BOT_TOKEN:-}

# Optional: VK API Configuration (if using VK parser)
ACCESS_TOKEN=${ACCESS_TOKEN:-}

# Optional: LLM Configuration (if using GigaChat)
SB_AUTH_DATA=${SB_AUTH_DATA:-}

# Optional: Cache settings
CACHE_TTL=${CACHE_TTL:-300}
EOF

# Устанавливаем безопасные права
chmod 600 "$ENV_FILE"

echo "✅ .env файл создан: $ENV_FILE"
echo "🔒 Права установлены: 600 (только владелец может читать/писать)"

# Показываем содержимое (без секретов)
echo ""
echo "📋 Содержимое .env файла:"
echo "========================"
sed 's/=.*/=***/' "$ENV_FILE" | grep -v "^#"
echo "========================"
