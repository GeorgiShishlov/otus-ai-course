# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack "Mini-Survey" app: Django REST API backend + Next.js frontend, containerized with Docker Compose.

## Structure

```
homework-1-full-stack/
├── docker-compose.yml
├── back/          # Django backend (port 8000)
└── front/         # Next.js frontend (port 3000)
```

## Running the project

### With Docker (production-like)
```bash
docker-compose up -d
```

### Backend locally
```bash
cd back
venv\Scripts\Activate.ps1        # PowerShell
# or: source venv/Scripts/activate  # bash/zsh
python manage.py runserver
```

### Frontend locally
```bash
cd front
npm run dev
```

## Backend (Django)

- **Django 6 + DRF** — `back/config/` holds settings and root URLs
- **App:** `back/survey/` — models, views, urls, renderers
- **API endpoints:** `GET /questions`, `GET /answers`, `POST /answers`
- **Model:** `SurveyAnswer` with `answers` (JSONField) and `created_at`
- **Custom renderer:** `survey/renderers.py` — `UTF8JSONRenderer` forces `ensure_ascii=False` so Cyrillic is stored and returned as-is
- **CORS:** `CORS_ALLOW_ALL_ORIGINS = True` (dev only)

After adding/changing models:
```bash
python manage.py makemigrations
python manage.py migrate
```

Seed the database via shell:
```bash
python manage.py shell -c "from survey.models import SurveyAnswer; SurveyAnswer.objects.create(answers=[...])"
```

## Frontend (Next.js)

- **Next.js 16 + React 19 + Tailwind CSS 3** — all UI in `front/src/app/page.tsx`
- Single `'use client'` page: fetches questions on mount, posts answers on submit, shows thank-you screen
- API base URL via `NEXT_PUBLIC_API_URL` env var (falls back to `http://localhost:8000`)
- Tailwind config at `front/tailwind.config.js`, globals at `front/src/app/globals.css`

If you see a hydration mismatch, clear the cache:
```bash
rm -rf front/.next
```
