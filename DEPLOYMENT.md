# ML-API Deployment Guide

## 🚀 Автоматический деплой через GitHub Actions

### Настройка GitHub Secrets

Добавьте следующие секреты в настройках репозитория (`Settings → Secrets and variables → Actions`):

#### Серверные настройки:
```bash
ML_API_SERVER_HOST=your-server-ip-or-domain
ML_API_SERVER_USER=deploy
ML_API_SERVER_PORT=22
ML_API_SERVER_PROJECT_PATH=/opt/ml-api
ML_API_SERVER_SSH_KEY=your_ssh_private_key_content
```

#### Конфигурация приложения:
```bash
# Обязательные секреты
PETS_DATABASE_PATH=https://storage.yandexcloud.net/pet-match-s3-storage/PetMatch/db.json

# API Configuration
API_URL=http://your-server:8001                    # URL ML-API сервиса (для самоссылок)

# Опциональные секреты (если используются соответствующие функции)
BOT_TOKEN=your_telegram_bot_token
ACCESS_TOKEN=your_vk_api_token
SB_AUTH_DATA=your_gigachat_auth_data
CACHE_TTL=300
```

### Подготовка сервера

1. **Создайте пользователя для деплоя:**
```bash
sudo useradd -m -s /bin/bash deploy
sudo usermod -aG docker deploy
```

2. **Настройте SSH ключи:**
```bash
# Создайте SSH ключ для деплоя
ssh-keygen -t rsa -b 4096 -C "ml-api-deploy" -f ~/.ssh/ml_api_deploy_key

# Скопируйте публичный ключ на сервер
ssh-copy-id -i ~/.ssh/ml_api_deploy_key.pub deploy@your-server

# Добавьте приватный ключ в GitHub Secret ML_API_SERVER_SSH_KEY
cat ~/.ssh/ml_api_deploy_key
```

3. **Подготовьте директорию проекта:**
```bash
# На сервере
sudo mkdir -p /opt/ml-api
sudo chown deploy:deploy /opt/ml-api

# Клонируйте репозиторий
sudo -u deploy git clone https://github.com/Pet-Match-ITMO/ML-API.git /opt/ml-api
```

### Процесс деплоя

#### Автоматический деплой:
- **При Push в master** → автоматический деплой в продакшен
- **При Pull Request** → сборка тестового образа

#### Ручной деплой:
```bash
# На сервере
cd /opt/ml-api
./deploy-ml-api.sh
```

### Мониторинг

#### Проверка статуса:
```bash
# Статус контейнеров
docker compose -f docker-compose.prod.yaml ps

# Логи сервиса
docker compose -f docker-compose.prod.yaml logs -f ml-api

# Проверка API
curl http://localhost:8001/
```

#### Health Check:
API включает автоматические проверки здоровья:
- Интервал: 30 секунд
- Таймаут: 10 секунд
- Повторы: 3 раза

### Troubleshooting

#### Проблемы с деплоем:
1. Проверьте GitHub Actions логи
2. Проверьте SSH подключение к серверу
3. Убедитесь что все секреты настроены

#### Проблемы с API:
1. Проверьте логи контейнера
2. Убедитесь что S3 URL доступен
3. Проверьте переменные окружения

### Rollback

Для отката к предыдущей версии:
```bash
# На сервере
cd /opt/ml-api

# Откат к предыдущему коммиту
git log --oneline -5
git checkout <previous-commit-hash>

# Перезапуск с предыдущей версией
./deploy-ml-api.sh
```

## 🔧 Локальная разработка

### Запуск для разработки:
```bash
# Создайте .env файл
echo "PETS_DATABASE_PATH=https://storage.yandexcloud.net/pet-match-s3-storage/PetMatch/db.json" > .env

# Запустите через Docker
docker compose up -d --build

# Или локально
pip install -r requirements.txt
python api.py
```

### Тестирование:
```bash
# Запуск тестов
python -m pytest

# Проверка кода
flake8 .
black --check .
isort --check-only .
```
