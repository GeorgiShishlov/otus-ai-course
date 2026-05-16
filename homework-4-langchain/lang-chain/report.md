# Отчёт: минимальный агент на LangChain

## LLM и настройка

**Модель:** `gpt-4o-mini` через [ProxyAPI](https://proxyapi.ru)

**Настройка:**
1. Зарегистрироваться и получить ключ на proxyapi.ru
2. Скопировать `.env.example` → `.env`
3. Заполнить переменные:
```
PROXYAPI_KEY=ваш-ключ
OPENAI_BASE_URL=https://api.proxyapi.ru/openai/v1
```

---

## API и поддерживаемые операции

**API:** [JSONPlaceholder](https://jsonplaceholder.typicode.com) — публичное тестовое REST API.

| Операция | HTTP-метод | Эндпоинт | Tool агента |
|---|---|---|---|
| Получить пост по ID | GET | `/posts/{id}` | `get_post` |
| Получить все посты пользователя | GET | `/posts?userId={id}` | `get_user_posts` |
| Создать новый пост | POST | `/posts` | `create_post` |

---

## Как запустить

```bash
# 1. Активировать виртуальное окружение
venv\Scripts\activate

# 2. Установить зависимости (один раз)
pip install -r requirements.txt

# 3. Настроить .env (скопировать из .env.example и вставить ключи)

# 4. Запустить агента
python my_agent.py "Дай мне пост номер 5"
```

---

## 5 тестовых запросов и результаты

### 1. Получить пост по ID → `get_post` (вызов API)

**Команда:**
```
python my_agent.py "Дай мне пост номер 5"
```

**Вывод агента:**
```
> Entering new AgentExecutor chain...

Invoking: `get_post` with `{'post_id': 5}`

[API] Запрашиваем пост с id=5

Status: success
Action: вызван get_post с id=5
Data: {"userId": 1, "id": 5, "title": "nesciunt quas odio", "body": "repudiandae veniam quaerat sunt sed\nalias aut fugiat sit autem sed est\nvoluptatem omnis possimus esse voluptatibus quis\nest aut tenetur dolor neque"}
Errors: None

> Finished chain.

📝 Итоговый ответ агента:
Status: success
Action: вызван get_post с id=5
Data: {"userId": 1, "id": 5, "title": "nesciunt quas odio", "body": "repudiandae veniam quaerat sunt sed\nalias aut fugiat sit autem sed est\nvoluptatem omnis possimus esse voluptatibus quis\nest aut tenetur dolor neque"}
Errors: None
```

---

### 2. Получить все посты пользователя → `get_user_posts` (вызов API)

**Команда:**
```
python my_agent.py "Покажи все посты пользователя с id 2"
```

**Вывод агента:**
```
> Entering new AgentExecutor chain...

Invoking: `get_user_posts` with `{'user_id': 2}`

[API] Запрашиваем посты пользователя с id=2

Status: success
Action: вызван get_user_posts с user_id=2
Data: [{"userId":2,"id":11,"title":"et ea vero quia laudantium autem","body":"..."},
       {"userId":2,"id":12,"title":"in quibusdam tempore odit est dolorem","body":"..."},
       ... (10 постов всего, id: 11–20)]
Errors: None

> Finished chain.

📝 Итоговый ответ агента:
Status: success
Action: вызван get_user_posts с user_id=2
Data: 10 постов пользователя 2 (id: 11–20), первый: {"userId":2,"id":11,"title":"et ea vero quia laudantium autem","body":"delectus reiciendis molestiae occaecati..."}
Errors: None
```

---

### 3. Создать пост → `create_post` (вызов API)

**Команда:**
```
python my_agent.py "Создай пост с заголовком «Мой первый пост», текстом «Привет, мир» и userId=1"
```

**Вывод агента:**
```
> Entering new AgentExecutor chain...

Invoking: `create_post` with `{'title': 'Мой первый пост', 'body': 'Привет, мир', 'userId': 1}`

[API] Создаем новый пост для пользователя с id=1

Status: success
Action: вызван create_post с заголовком «Мой первый пост»
Data: {"title":"Мой первый пост","body":"Привет, мир","userId":1,"id":101}
Errors: None

> Finished chain.

📝 Итоговый ответ агента:
Status: success
Action: вызван create_post с заголовком «Мой первый пост»
Data: {"title":"Мой первый пост","body":"Привет, мир","userId":1,"id":101}
Errors: None
```

---

### 4. Запрос вне области API → отказ без вызова инструментов

**Команда:**
```
python my_agent.py "Напиши шутку"
```

**Вывод агента:**
```
> Entering new AgentExecutor chain...
Status: error
Action: None
Data: None
Errors: "Не могу выполнить запрос на создание шутки."

> Finished chain.

📝 Итоговый ответ агента:
Status: error
Action: None
Data: None
Errors: "Не могу выполнить запрос на создание шутки."
```

---

### 5. Получить посты пользователя 3 → `get_user_posts` (вызов API)

**Команда:**
```
python my_agent.py "Какой пост у пользователя 3?"
```

**Вывод агента:**
```
> Entering new AgentExecutor chain...

Invoking: `get_user_posts` with `{'user_id': 3}`

[API] Запрашиваем посты пользователя с id=3

Status: success
Action: вызван get_user_posts с user_id=3
Data: [{"userId":3,"id":21,"title":"asperiores ea ipsam voluptatibus modi minima quia sint","body":"..."},
       {"userId":3,"id":22,"title":"dolor sint quo a velit explicabo quia nam","body":"..."},
       ... (10 постов всего, id: 21–30)]
Errors: None

> Finished chain.

📝 Итоговый ответ агента:
Status: success
Action: вызван get_user_posts с user_id=3
Data: 10 постов пользователя 3 (id: 21–30), первый: {"userId":3,"id":21,"title":"asperiores ea ipsam voluptatibus modi minima quia sint","body":"repellat aliquid praesentium dolorem quo..."}
Errors: None
```

---

## Используемые промпты

### Системный промпт (`my_agent.py`, строки 58–74)

```
Ты — API-оператор. У тебя есть доступ к трём инструментам:
1. get_post(post_id) — получить пост по ID.
2. get_user_posts(user_id) — получить все посты пользователя.
3. create_post(title, body, userId) — создать новый пост.

Всегда отвечай строго в формате:

Status: success | error
Action: какое действие выполнил (например, "вызван get_post с id=3")
Data: результат API в удобном виде (если ошибка, то "None")
Errors: описание ошибки или "None"

Если пользователь спрашивает про пост — используй get_post.
Если про все посты пользователя — get_user_posts.
Если про создание — create_post.
Никогда не выдумывай данные — только вызывай инструменты.
```

### Пользовательский шаблон

Запрос передаётся напрямую из CLI:
```bash
python my_agent.py "<запрос на естественном языке>"
```

| Намерение | Пример запроса | Вызываемый tool |
|---|---|---|
| Получить пост | "Дай мне пост номер 5" | `get_post` |
| Посты пользователя | "Покажи все посты пользователя 2" | `get_user_posts` |
| Создать пост | "Создай пост с заголовком ..." | `create_post` |
| Вне области | "Напиши шутку" | _(не вызывается)_ |

---

## Подтверждение критериев оценки

| Критерий | Где в репозитории |
|---|---|
| Агент запускается | `python my_agent.py "запрос"` |
| Tool с реальным HTTP-вызовом | `my_agent.py:17–43`, вызовы через `requests` |
| Debug-вывод tool | `my_agent.py`, строки `print(f"[API] ...")` |
| Пример: запрос → API-метод | "Дай мне пост номер 5" → `get_post` → `GET /posts/5` |
| Контракт ответа | системный промпт, `my_agent.py:58–74` |
| 5 тестовых запросов | раздел выше |
| Промпты оформлены | раздел «Используемые промпты» |
| Секреты не закоммичены | `.gitignore` исключает `.env` |
