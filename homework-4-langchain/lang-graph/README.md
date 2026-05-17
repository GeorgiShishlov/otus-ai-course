# LangGraph Agent — JSONPlaceholder API

Минимальный AI-агент на **LangGraph**, который принимает запросы на естественном языке и вызывает JSONPlaceholder API через инструменты.

## Стек

| Компонент | Версия |
|-----------|--------|
| LangGraph | 1.2.0 |
| LangChain | 1.3.1 |
| LLM | gpt-4o-mini (через ProxyAPI) |
| API | [JSONPlaceholder](https://jsonplaceholder.typicode.com) |

## Структура проекта

```
lang-graph/
├── agent.py          # Граф агента (StateGraph)
├── tools.py          # LangChain-инструменты (API-вызовы)
├── requirements.txt
├── .env.example
└── README.md
```

## Настройка окружения

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Скопируйте `.env.example` в `.env` и заполните ключи:

```powershell
copy .env.example .env
```

```env
PROXYAPI_KEY=your_proxyapi_key_here
OPENAI_BASE_URL=https://api.proxyapi.ru/openai/v1
```

## Запуск

```powershell
python agent.py
```

Агент запускается в интерактивном режиме. Для выхода введите `exit` или `quit`.

## Поддерживаемые API-операции

| Инструмент | Описание | Пример запроса |
|---|---|---|
| `get_post(post_id)` | Получить пост по ID | «покажи пост 1» |
| `get_user_posts(user_id)` | Получить все посты пользователя | «покажи все посты пользователя 3» |

## Контракт ответа

Агент всегда отвечает в формате:

```
Status: success/error
Action: что сделал
Data: результат API
Errors: ошибки или None
```

Описание формата задано в системном промпте (`SYSTEM_PROMPT` в `agent.py`).

## Архитектура графа

```
START → agent → [tools_condition]
                    ├── tool_calls? → tools → agent (цикл)
                    └── нет?        → END
```

- **agent** — узел с LLM, принимает решение о вызове инструментов
- **tools** — узел `ToolNode`, выполняет API-вызовы
- **tools_condition** — встроенная функция LangGraph, роутит по наличию `tool_calls`
- **InMemorySaver** — checkpointer для сохранения истории диалога
