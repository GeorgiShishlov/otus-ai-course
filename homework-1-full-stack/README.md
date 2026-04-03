# Мини-анкета — Homework 1

Учебный проект курса **AI для разработчиков** (OTUS).  
Простое full-stack приложение: Django backend + Next.js frontend.

---

## Функционал

- `GET /questions` — возвращает 5 вопросов анкеты
- `POST /answers` — сохраняет ответы пользователя в SQLite
- `GET /answers` — возвращает все сохранённые ответы
- Frontend загружает вопросы с backend, принимает ответы и показывает сообщение «Спасибо!»

---

## Стек

| Часть          | Технологии                                   |
| -------------- | -------------------------------------------- |
| Backend        | Python 3.12, Django 6, Django REST Framework |
| Frontend       | Next.js 16, React 19, Tailwind CSS 3         |
| База данных    | SQLite                                       |
| Инфраструктура | Docker, Docker Compose                       |

---

## Запуск

### Требования

- [Docker](https://www.docker.com/) и Docker Compose

### Команда запуска

```bash
git clone https://github.com/GeorgiShishlov/otus-ai-course.git
cd homework-1-full-stack
docker-compose up -d
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000](http://localhost:8000)

### Остановка

```bash
docker-compose down
```

### Начальные данные

При первом запуске база данных автоматически заполняется примером заполненной анкеты (5 ответов на вопросы о JavaScript и REST API). Это происходит через data migration `survey/migrations/0002_seed_answers.py`, которая выполняется как часть `migrate` при старте контейнера.

---

## Скриншоты

> _Добавьте скриншоты в папку `screenshots/` и вставьте их сюда_

```
screenshots/
├── 01-form.png        — форма с вопросами
├── 02-submitted.png   — экран «Спасибо!»
└── 03-answers.png     — GET /answers в браузере
```

---

## Использованные промпты

Проект разработан с использованием **Claude Code** (AI-ассистент в IDE).

### Backend

> Я хочу создать Django бэкенд для моего Next.js проекта. Помоги мне настроить всё с нуля.  
> Backend предоставляет два API:  
> GET /questions — возвращает список вопросов анкеты (жёстко заданных, 5 шт.).  
> POST /answers — принимает ответы пользователя и сохраняет их в памяти

---

> добавь, пожалуйста, SQLite

---

> где можно посмотреть сохраненные ответы?

### Frontend

> нужно написать вопрос для студента, окно для ответа, пока никуда не отправляется

---

> нужно сделать с tailwind 3. Заголовок: Мини-анкета.  
> Frontend: загружает 5 вопросов с backend; отображает; отправляет заполненные ответы через POST /answers; показывает пользователю сообщение «Спасибо!» после отправки.

### Docker

> нужно обернуть все это в docker.  
> Требование преподавателя: чтобы после скачивания с github все запускалось по команде: docker-compose up -d

### Отладка

> русские слова искажаются: ["\u043f\u0440\u0438\u0432\u0435\u0442", ...]  
> латинские сохраняет хорошо

---

## Структура проекта

```
homework-1-full-stack/
├── docker-compose.yml
├── back/                  # Django backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── config/            # Настройки Django
│   └── survey/            # Приложение (модели, views, urls)
└── frond/                 # Next.js frontend
    ├── Dockerfile
    └── src/app/page.tsx   # Главная страница анкеты
```
