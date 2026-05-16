# LangChain Agent — JSONPlaceholder API

Минимальный AI-агент на LangChain: обёртка на естественном языке над публичным REST API.

## Что умеет

Принимает запрос на русском языке и вызывает нужный метод [JSONPlaceholder API](https://jsonplaceholder.typicode.com):

| Запрос пользователя | Вызываемый tool | API-метод |
|---|---|---|
| "Дай мне пост номер 5" | `get_post` | GET `/posts/5` |
| "Покажи все посты пользователя 2" | `get_user_posts` | GET `/posts?userId=2` |
| "Создай пост с заголовком ..." | `create_post` | POST `/posts` |

## Стек

- **LLM:** GPT-4o-mini через [ProxyAPI](https://proxyapi.ru)
- **Фреймворк:** LangChain + langchain-classic

## Установка

```bash
# 1. Создать и активировать виртуальное окружение
python -m venv venv
venv\Scripts\activate

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Настроить переменные окружения
copy .env.example .env
# Открыть .env и вставить свой PROXYAPI_KEY
```

## Запуск

```bash
python my_agent.py "Дай мне пост номер 5"
python my_agent.py "Покажи все посты пользователя с id=2"
python my_agent.py "Создай пост с заголовком «Тест», текстом «Привет» и userId=1"
```

## Формат ответа

Агент всегда отвечает в фиксированном формате:

```
Status: success | error
Action: описание выполненного действия
Data: результат API
Errors: описание ошибки или None
```

## Структура проекта

```
lang-chain/
├── my_agent.py       # агент, tools, prompt, запуск
├── report.md         # отчёт с тестовыми запросами и промптами
├── requirements.txt
├── .env.example
└── .gitignore
```

Подробнее — в [report.md](report.md).
