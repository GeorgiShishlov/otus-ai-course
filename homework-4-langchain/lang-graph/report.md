# Отчёт: LangGraph Agent

## LLM и настройка

**Модель:** `gpt-4o-mini` через [ProxyAPI](https://proxyapi.ru)

Настройка в `.env`:
```env
PROXYAPI_KEY=your_proxyapi_key_here
OPENAI_BASE_URL=https://api.proxyapi.ru/openai/v1
```

## API и поддерживаемые операции

**API:** [JSONPlaceholder](https://jsonplaceholder.typicode.com) — публичное тестовое REST API.

| Операция | Метод | Инструмент | Файл |
|---|---|---|---|
| Получить пост по ID | `GET /posts/{id}` | `get_post` | `tools.py:L8–L18` |
| Получить посты пользователя | `GET /users/{id}/posts` | `get_user_posts` | `tools.py:L21–L31` |

Реальные HTTP-вызовы выполняются через `requests.get()`. Debug-вывод (`[API] Запрос ...`) добавлен в каждый инструмент (`tools.py:L10`, `tools.py:L23`).

## Как запустить

```powershell
# Создать и активировать venv
python -m venv venv
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Настроить ключи
copy .env.example .env
# отредактировать .env

# Запустить агента
python agent.py
```

## 5 тестовых запросов

### Запрос 1 — получить пост по ID (вызов API)

```
Вы: покажи пост 1
[API] Запрос поста 1

Агент: Status: success
Action: Получил пост по ID 1
Data: {"userId":1,"id":1,"title":"sunt aut facere repellat provident occaecati excepturi optio reprehenderit","body":"quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"}
Errors: None
```

**API-вызов:** `get_post(post_id=1)` → `GET /posts/1`

---

### Запрос 2 — получить посты пользователя (вызов API)

```
Вы: покажи все посты пользователя 3
[API] Запрос постов пользователя 3

Агент: Status: success
Action: Получил все посты пользователя с ID 3
Data: [
  {"userId":3,"id":21,"title":"asperiores ea ipsam voluptatibus modi minima quia sint","body":"repellat aliquid praesentium dolorem quo\nsed totam minus non itaque\nnihil labore molestiae sunt dolor eveniet hic recusandae veniam\ntempora et tenetur expedita sunt"},
  {"userId":3,"id":22,"title":"dolor sint quo a velit explicabo quia nam","body":"eos qui et ipsum ipsam suscipit aut\nsed omnis non odio\nexpedita earum mollitia molestiae aut atque rem suscipit\nnam impedit esse"},
  ...всего 10 постов...
]
Errors: None
```

**API-вызов:** `get_user_posts(user_id=3)` → `GET /users/3/posts`

---

### Запрос 3 — запрос без вызова API

```
Вы: Расскажи шутку

Агент: Почему программисты не любят природу?

Потому что в ней слишком много багов!
```

**API-вызов:** нет — агент ответил самостоятельно, инструменты не потребовались.

---

### Запрос 4 — получить другой пост (вызов API)

```
Вы: дай мне пост номер 5
[API] Запрос поста 5

Агент: Status: success
Action: Получил пост по ID 5
Data: {"userId":1,"id":5,"title":"nesciunt quas odio","body":"repudiandae veniam quaerat sunt sed\nalias aut fugiat sit autem sed est\nvoluptatem omnis possimus esse voluptatibus quis\nest aut tenetur dolor neque"}
Errors: None
```

**API-вызов:** `get_post(post_id=5)` → `GET /posts/5`

---

### Запрос 5 — посты другого пользователя (вызов API)

```
Вы: какие посты написал пользователь 1?
[API] Запрос постов пользователя 1

Агент: Status: success
Action: Получил все посты пользователя с ID 1
Data: [
  {"userId":1,"id":1,"title":"sunt aut facere repellat provident occaecati excepturi optio reprehenderit","body":"quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"},
  {"userId":1,"id":2,"title":"qui est esse","body":"est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"},
  {"userId":1,"id":3,"title":"ea molestias quasi exercitationem repellat qui ipsa sit aut","body":"et iusto sed quo iure\nvoluptatem occaecati omnis eligendi aut ad\nvoluptatem doloribus vel accusantium quis pariatur\nmolestiae porro eius odio et labore et velit aut"},
  {"userId":1,"id":4,"title":"eum et est occaecati","body":"ullam et saepe reiciendis voluptatem adipisci\nsit amet autem assumenda provident rerum culpa\nquis hic commodi nesciunt rem tenetur doloremque ipsam iure\nquis sunt voluptatem rerum illo velit"},
  {"userId":1,"id":5,"title":"nesciunt quas odio","body":"repudiandae veniam quaerat sunt sed\nalias aut fugiat sit autem sed est\nvoluptatem omnis possimus esse voluptatibus quis\nest aut tenetur dolor neque"},
  {"userId":1,"id":6,"title":"dolorem eum magni eos aperiam quia","body":"ut aspernatur corporis harum nihil quis provident sequi\nmollitia nobis aliquid molestiae\nperspiciatis et ea nemo ab reprehenderit accusantium quas\nvoluptate dolores velit et doloremque molestiae"},
  {"userId":1,"id":7,"title":"magnam facilis autem","body":"dolore placeat quibusdam ea quo vitae\nmagni quis enim qui quis quo nemo aut saepe\nquidem repellat excepturi ut quia\nsunt ut sequi eos ea sed quas"},
  {"userId":1,"id":8,"title":"dolorem dolore est ipsam","body":"dignissimos aperiam dolorem qui eum\nfacilis quibusdam animi sint suscipit qui sint possimus cum\nquaerat magni maiores excepturi\nipsam ut commodi dolor voluptatum modi aut vitae"},
  {"userId":1,"id":9,"title":"nesciunt iure omnis dolorem tempora et accusantium","body":"consectetur animi nesciunt iure dolore\nenim quia ad\nveniam autem ut quam aut nobis\net est aut quod aut provident voluptas autem voluptas"},
  {"userId":1,"id":10,"title":"optio molestias id quia eum","body":"quo et expedita modi cum officia vel magni\ndoloribus qui repudiandae\nvero nisi sit\nquos veniam quod sed accusamus veritatis error"}
]
Errors: None
```

**API-вызов:** `get_user_posts(user_id=1)` → `GET /users/1/posts`

---

## Использованные промпты

### Системный промпт (agent.py)

```
Ты — API-оператор. У тебя есть доступ к инструментам:
- get_post(post_id) — получить пост по ID
- get_user_posts(user_id) — получить все посты пользователя

Всегда отвечай в формате:
Status: success/error
Action: что сделал
Data: результат API
Errors: ошибки или None
```

**Назначение:** задаёт роль агента, перечисляет доступные инструменты, устанавливает обязательный контракт ответа.

### Описания инструментов (tools.py)

```python
"""Получить пост по ID из JSONPlaceholder API"""
```
```python
"""Получить все посты пользователя по его ID"""
```

**Назначение:** docstring инструмента передаётся в LLM как описание функции — именно по нему модель решает, какой инструмент вызывать.

### Пользовательские запросы (примеры)

| Запрос | Ожидаемое действие |
|---|---|
| «покажи пост 1» | вызов `get_post(1)` |
| «покажи все посты пользователя 3» | вызов `get_user_posts(3)` |
| «дай мне пост номер 5» | вызов `get_post(5)` |
| «какие посты написал пользователь 1» | вызов `get_user_posts(1)` |
| «расскажи шутку» | ответ без вызова инструментов |
