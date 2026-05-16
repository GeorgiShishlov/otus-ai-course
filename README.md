# OTUS — AI для разработчиков

Репозиторий с домашними заданиями курса **[AI для разработчиков](https://otus.ru/)** (OTUS).

Автор: Юрий Шишлов

---

## Домашние задания

### ДЗ 1 — Мини-анкета (full-stack)

Стек: Django, Next.js, Docker

Папка: `homework-1-full-stack`

---

### ДЗ 2 — Ревью кода opensource проекта

Стек: Node.js, Express 4, Passport.js, SQLite3, EJS

Папка: `homework-2-onboarding`

Проект: [todos-express-password](https://github.com/passport/todos-express-password) — эталонный пример аутентификации по паролю от авторов Passport.js.

**Результат ревью:** homework-2-onboarding/todos-express-password/REVIEW.md

---

### ДЗ 3 — Дополнение проекта инструкциями для ИИ

Папка: `homework-3-architecture/json-todo-cli-mvp`

Проект: учебный Python CLI для управления задачами (3-слойная архитектура: CLI → Service → JSON Storage).

**Что сделано:**
- Добавлен `CLAUDE.md` — инструкции для Claude Code: контекст проекта, карта модулей, глоссарий, ограничения, правила кода и тестов, формат ответа агента, 4 типовых сценария с промптами и Definition of Done, Known Issues, раздел с использованными промптами.
- Проверочное требование §8: каждый изменённый `.py` файл должен начинаться с `# [TODO-MVP]` — машинопроверяемое доказательство следования инструкциям.
- Практическая проверка через агента: выполнены три задачи по сценариям из `CLAUDE.md` — написание тестов, исправление бага, рефакторинг.
- Добавлена C4-модель архитектуры (`workspace.dsl`) — 4 диаграммы: System Context, Containers, Components (Console App), Components (JSON Files).
- Добавлена диаграмма классов (`class_diagram.puml`) — C4 Level 4: все классы, атрибуты, методы и связи.

**Просмотр C4-модели (Structurizr):**
```powershell
docker run -it --rm -p 8080:8080 `
  -v "PATH_TO_PROJECT:/usr/local/structurizr" `
  structurizr/structurizr local
```
Открыть: http://localhost:8080

**Просмотр диаграммы классов (PlantUML):**

Способ 1 — онлайн: открыть [plantuml.com/plantuml](https://www.plantuml.com/plantuml/uml/), вставить содержимое `class_diagram.puml`.

Способ 2 — VS Code: установить расширение **PlantUML** (jebbs), открыть файл, нажать `Alt+D`.

Способ 3 — IntelliJ / PyCharm: плагин **PlantUML Integration**, превью открывается автоматически.

**Добавлены три Claude Code skills** (`.agents/skills/`):

| Skill | Описание |
|-------|----------|
| `jest-testing` | Тестирование Node.js приложений с Jest: unit, integration, mocking, coverage, CI/CD |
| `nodejs-best-practices` | Принципы Node.js разработки: выбор фреймворка, async-паттерны, безопасность, архитектура |
| `nodejs-express-server` | Построение production-ready Express.js серверов: middleware, auth, routing, БД |

---

### ДЗ 4 — Минимальный агент на LangChain

Стек: Python, LangChain, langchain-classic, GPT-4o-mini (ProxyAPI)

Папка: `homework-4-langchain/lang-chain`

**Что сделано:**
- Агент принимает запрос на естественном языке и вызывает нужный метод публичного API [JSONPlaceholder](https://jsonplaceholder.typicode.com)
- Реализованы 3 LangChain-инструмента: `get_post`, `get_user_posts`, `create_post` — с реальными HTTP-вызовами через `requests`
- Системный промпт задаёт роль API-оператора, ограничения и фиксированный формат ответа
- Запуск из CLI: `python my_agent.py "Дай мне пост номер 5"`

**Формат ответа агента:**
```
Status: success | error
Action: описание действия
Data: результат API
Errors: описание ошибки или None
```

**Запуск:**
```powershell
cd homework-4-langchain/lang-chain
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # вставить PROXYAPI_KEY
python my_agent.py "Дай мне пост номер 5"
```

**Отчёт и промпты:** `homework-4-langchain/lang-chain/report.md`

---

### ДЗ 5 — _(в разработке)_
