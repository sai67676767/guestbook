# Todo-list на Docker Compose

## Описание проекта

Todo-list (список задач), собранный в Docker Compose. Проект работает на трёх контейнерах: nginx, backend (Python) и база данных (PostgreSQL).

## Возможности

- Добавление задачи
- Отметка задачи выполненной
- Удаление задачи

## Стек технологий

- **Backend:** Python + FastAPI
- **База данных:** PostgreSQL
- **Frontend:** HTML + CSS + JavaScript
- **Веб-сервер:** Nginx
- **Контейнеризация:** Docker + Docker Compose

## Структура репозитория

Проект состоит из трёх папок: `backend`, `frontend`, `nginx`.

**backend** — тут лежит код на Python. Внутри три файла:
- `main.py` — с логикой API
- `requirements.txt` — со списком библиотек
- `Dockerfile` — инструкция для контейнера

**frontend** — тут файл `index.html`. Это HTML-страница с полем ввода, списком задач и кнопками. CSS и JavaScript встроены прямо в файл.

**nginx** — тут файл `nginx.conf`. Он говорит, что отдавать и куда перенаправлять запросы.

Ещё в корне проекта:
- `docker-compose.yml` — инструкция работы контейнеров и их взаимодействия
- `.env.example` — шаблон переменных окружения
- `.gitignore` — файл, который говорит Git, что не нужно выкладывать
- `README.md` — этот файл

## Установка и запуск

### Требования:
- Docker
- Docker Compose

### Запуск:
```bash
docker compose up -d --build
