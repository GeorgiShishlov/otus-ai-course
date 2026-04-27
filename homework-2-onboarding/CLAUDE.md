# CLAUDE.md

Этот файл содержит инструкции для Claude Code (claude.ai/code) при работе с данным репозиторием.

## Команды

```bash
npm install   # установить зависимости
npm start     # запустить сервер на http://localhost:3000
```

Скрипты для линтинга и тестов не настроены.

## Архитектура

Традиционное серверное веб-приложение (без клиентского фреймворка). Вся логика выполняется на сервере: браузер отправляет HTML-формы и получает в ответ готовые HTML-страницы.

### Жизненный цикл запроса

1. `bin/www` — создаёт HTTP-сервер и слушает порт `PORT` (по умолчанию 3000).
2. `app.js` — настраивает стек middleware Express в следующем порядке: логгер → парсинг тела → cookie → статические файлы → сессия → CSRF → восстановление сессии Passport → флеш-сообщения → роутеры → 404 → обработчик ошибок.
3. `routes/auth.js` — обрабатывает `/login`, `/login/password`, `/logout`, `/signup`. Также содержит настройку `LocalStrategy` и `serializeUser`/`deserializeUser`. Регистрируются как побочный эффект при первом `require` модуля.
4. `routes/index.js` — весь CRUD задач (`/`, `/active`, `/completed`, `/:id`, `/toggle-all`, `/clear-completed`). Все маршруты, кроме `GET /`, требуют middleware `ensureLoggedIn`.
5. `db.js` — открывает базу данных SQLite, создаёт таблицы `users` и `todos` если их нет, добавляет начального пользователя `alice / letmein`. Экспортируется как синглтон `db`, используемый напрямую в обоих файлах роутов.

### Поток аутентификации

- **Стратегия:** `passport-local` — читает `username` и `password` из тела POST-запроса, ищет пользователя в SQLite, проверяет пароль через `crypto.pbkdf2` + `crypto.timingSafeEqual`.
- **Хранилище сессий:** `connect-sqlite3` записывает сессии в `./var/db/sessions.db`. Cookie сессии называется `connect.sid`.
- **Содержимое сессии:** сериализуется только `{ id, username }` (не вся строка пользователя). `deserializeUser` восстанавливает этот объект прямо из сессии, без дополнительного запроса к БД.
- **CSRF:** middleware `csurf` добавляет `req.csrfToken()`; каждая мутирующая форма включает скрытое поле `_csrf`, заполненное из `res.locals.csrfToken`.

### Модель данных

Две таблицы SQLite в `./var/db/todos.db`:

- `users(id, username UNIQUE, hashed_password BLOB, salt BLOB)`
- `todos(id, owner_id NOT NULL, title NOT NULL, completed INTEGER)`

`completed` хранится как `1` (выполнено) или `NULL` (не выполнено) — не как булево значение.

### Шаблоны

EJS-шаблоны в `views/`. Шаблон `index.ejs` обслуживает все три фильтра списка (все / активные / выполненные) через `res.locals.filter`. Хелпер `pluralize` доступен глобально через `app.locals.pluralize`.
