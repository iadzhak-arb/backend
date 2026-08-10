# Arbitrage — Backend (Django 6.0)

> **⚠️ DEPRECATED:** Этот модуль больше не поддерживается и находится в архиве для исторических целей и ознакомления.
> Вместо него теперь используются два отдельных репозитория:
> - **[auth](https://github.com/iadzhak-arb/auth)** — аутентификация
> - **[arb](https://github.com/iadzhak-arb/arb)** — арбитражная логика

Backend-сервис для отслеживания арбитражных возможностей на криптовалютных биржах. Реализует два независимых, но
связанных потока:

- **REST API** — предоставляет доступ к данным об арбитражных связках, ордербуках, биржах, токенах и сводной статистике.
- **Message Processing** — принимает данные из RabbitMQ (orderbooks), рассчитывает арбитражные возможности и сохраняет
  результаты в БД.

Сервис спроектирован в духе микросервисной архитектуры: API и обработка сообщений — это отдельные процессы, которые
могут масштабироваться независимо.

## Технологии

- **Python 3.14**
- **Django 6.0** — веб-фреймворк и ORM
- **Django REST Framework** — REST API
- **FastStream** — обработка сообщений (RabbitMQ)
- **SQLite** — БД по умолчанию (легко заменяется на PostgreSQL)
- **JWT-аутентификация** через `auth-kit` + `django-allauth`
- **OpenAPI/Swagger** — документация (`drf-spectacular`)

## Возможности

- Мониторинг ордербуков нескольких бирж в реальном времени (через RabbitMQ)
- Расчёт арбитражных возможностей: spot-spot, spot-swap
- REST API с пагинацией, фильтрацией и поиском (`Django Filter`, `PageLimitPagination`)
- Swagger-документация и OpenAPI-схема
- RabbitMQ-консьюмер для потоковой обработки orderbook-данных
- JWT-аутентификация с HttpOnly-куками (access/refresh)
- Сводная статистика по биржам, рынкам, токенам и арбитражным событиям

## Структура проекта

```text
backend/
├── api/                  # API-эндпоинты (views, serializers, filters)
├── backend/              # Настройки Django, URLs, брокер для RabbitMQ
├── orderbooks/           # Модели, консьюмеры, утилиты для orderbooks
├── users/                # Кастомная модель пользователя
├── manage.py
├── serve_faststream.py   # Запуск FastStream-консьюмера
├── server.sh             # Скрипт запуска Django API
└── faststream.sh         # Скрипт запуска FastStream-консьюмера
```

## Модели данных

| Модель          | Описание                          |
|-----------------|-----------------------------------|
| `Exchange`      | Биржа                             |
| `Token`         | Токен/актив                       |
| `Market`        | Рынок торговли                    |
| `Symbol`        | Торговая пара (base/quote/settle) |
| `Orderbook`     | Ордербук для пары на бирже        |
| `OrderbookData` | Снимок asks/bids в момент времени |
| `Arbitrage`     | Пара ордербуков (buy/sell)        |
| `ArbitrageData` | История расчётов маржи и объёмов  |

> **Важно:** `ArbitrageData` рассчитан на высокую нагрузку (до 7000 записей в минуту).

## API эндпоинты

| Метод | URL                     | Описание                               | Auth |
|-------|-------------------------|----------------------------------------|------|
| `GET` | `/arbitrage/`           | Список арбитражных возможностей        | ✅   |
| `GET` | `/arbitrage/{id}/`      | Детали конкретной возможности          | ✅   |
| `GET` | `/arbitrage/latest/`    | Последние данные за дельту времени     | ✅   |
| `GET` | `/arbitrage/demo-spot/` | Демо: spot-spot арбитраж               | —    |
| `GET` | `/arbitrage/demo-swap/` | Демо: spot-swap арбитраж               | —    |
| `GET` | `/arbitrage/{id}/back/` | Обратный арбитраж                      | ✅   |
| `GET` | `/summary/`             | Сводка: биржи, символы, сделки, аптайм | —    |
| `GET` | `/markets/`             | Список рынков                          | ✅   |
| `GET` | `/exchanges/`           | Список бирж                            | ✅   |
| `GET` | `/tokens/`              | Список токенов                         | ✅   |
| `GET` | `/tokens/base/`         | Base токены                            | ✅   |
| `GET` | `/tokens/quote/`        | Quote токены                           | ✅   |
| `GET` | `/tokens/settle/`       | Settle токены                          | ✅   |
| —     | `/auth/`                | Аутентификация (register, login, etc.) | —    |
| `GET` | `/schema/`              | OpenAPI schema                         | —    |
| `GET` | `/docs/`                | Swagger UI                             | —    |

## Установка и запуск

### Локально

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций (обязательно перед запуском)
cd backend
python manage.py migrate

# Запуск API-сервера
python manage.py runserver

# В другом терминале — запуск FastStream-консьюмера
python serve_faststream:app
```

### Запуск через скрипты

Оба скрипта применяют миграции и запускают свой функционал:

```bash
# Запуск Django API (server.sh)
./server.sh

# Запуск FastStream-консьюмера (faststream.sh)
./faststream.sh
```

> **Примечание:** Скрипты должны находиться в корне проекта (не в папке `backend/`).

### Docker

```bash
# Сборка и запуск
docker build -t arbitrage-backend .
docker run -p 80:80 arbitrage-backend
```

> **Ключевой момент:** Миграции применяются при каждом запуске контейнера через `server.sh` (entrypoint). Для продакшена
> рекомендуется выносить миграции в отдельный init-контейнер или применять вручную перед первым запуском, чтобы избежать
> гонок при масштабировании.

## Переменные окружения

| Переменная         | По умолчанию                        | Описание              |
|--------------------|-------------------------------------|-----------------------|
| `SECRET_KEY`       | random                              | Секретный ключ Django |
| `DEBUG`            | `True`                              | Режим отладки         |
| `ALLOWED_HOSTS`    | `localhost,127.0.0.1,192.168.0.100` | Разрешённые хосты     |
| `RMQ_HOST`         | `localhost`                         | Хост RabbitMQ         |
| `RMQ_PORT`         | `5672`                              | Порт RabbitMQ         |
| `RMQ_USER`         | `guest`                             | Пользователь RabbitMQ |
| `RMQ_PASS`         | `guest`                             | Пароль RabbitMQ       |
| `QUEUE_ORDERBOOKS` | `orderbooks`                        | Имя очереди           |

## Тестирование

Пока что не покрыто тестами

## Аутентификация и безопасность

Проект использует JWT-аутентификацию с cookie-based токенами:

- **Access Token**: 15 минут
- **Refresh Token**: 1 день
- Токены передаются через HttpOnly-куки (защита от XSS)
- Эндпоинт `/auth/` поддерживает регистрацию, логин, обновление токенов

Для продакшена обязательно:

- Отключите `DEBUG`
- Задайте надёжный `SECRET_KEY`
- Ограничьте `ALLOWED_HOSTS`
- Используйте HTTPS и настройте CORS

## Рекомендации по масштабированию

- API и FastStream-воркер можно масштабировать независимо (разные контейнеры, разные реплики)
- При высокой нагрузке замените SQLite на PostgreSQL
- Для балансировки нагрузки используйте Traefik или Nginx
- Очередь RabbitMQ можно вынести в отдельный кластер
