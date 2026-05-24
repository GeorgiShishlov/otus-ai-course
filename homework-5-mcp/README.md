# MCP‑сервер

Реализован MCP‑сервер — [server.py](server.py): L20–L104

## Принципы MCP

Главный принцип в том, чтобы клиент и сервер обменивались сообщениями, которые организованы по стандарту.
Позволяет AI-агенту вызывать внешние инструменты по стандартному протоколу.

Клиент (Claude Code) запускает сервер как отдельный процесс и общается с ним через **stdio** (stdin/stdout) по протоколу **JSON-RPC 2.0**.
Клиент читает список доступных инструментов при старте и сам решает, какой вызвать — на основе описания tool'а.

## Tools

Инструменты — это действия, которые ИИ может выполнить во внешней системе, например, найти файл по паттерну.

У каждого tool есть:

- `name` — уникальное имя (`read_file`)
- `description` — текст для модели: она читает его и решает, когда вызывать
- параметры — JSON Schema (что принимает функция)
- результат — JSON-ответ (что возвращает)

### Инструмент 1: получение описания термина из глоссария

[server.py: L25–L39](server.py)  
Логи: `server.py: L36`

Запрос и результат:
```
term: MCP
```
```json
{
  "term": "MCP",
  "description": "Model Context Protocol — протокол, разработанный Anthropic, суть в том, чтобы клиент и сервер обменивались сообщениями, которые организованы по стандарту. Позволяет AI-агенту вызывать внешние инструменты по стандартному протоколу.",
  "error": null
}
```

### Инструмент 2: чтение файла по пути (относительно PROJECT_ROOT)

[server.py: L44–L60](server.py)  
Логи: `server.py: L54–L59`

Запрос и результат:
```
path: requirements.txt
```
```json
{
  "path": "requirements.txt",
  "content": "mcp>=1.9.0\npython-dotenv>=1.0.0\npytest>=8.0.0",
  "error": null
}
```

### Инструмент 3: поиск текста в файлах проекта

[server.py: L65–L82](server.py)  
Логи: `server.py: L76–L81`

Запрос и результат:
```
query: pytest
```
```json
{
  "query": "pytest",
  "matches": [
    { "file": ".gitignore", "line": 5, "text": ".pytest_cache/" },
    { "file": "requirements.txt", "line": 3, "text": "pytest>=8.0.0" },
    { "file": "server.py", "line": 88, "text": "def tool_run_tests(command: str = \"pytest tests/ -v\") -> dict:" },
    { "file": "tools.py", "line": 34, "text": "ALLOWED_PREFIXES = [\"pytest\", \"python -m pytest\", \"flake8\", \"pip check\"]" }
  ],
  "error": null
}
```

### Инструмент 4: запуск команд из белого списка

[server.py: L88–L104](server.py)  
Логи: `server.py: L99–L103`

Разрешены: `pytest`, `python -m pytest`, `flake8`, `pip check`.

Запрос и результат:
```
command: pytest --version
```
```json
{
  "command": "pytest --version",
  "output": "pytest 9.0.3\n",
  "status": "success",
  "error": null
}
```

```
command: pip check
```
```json
{
  "command": "pip check",
  "output": "No broken requirements found.\n",
  "status": "success",
  "error": null
}
```

## Безопасность

- **Sandbox**: `read_file` и `search_files` ограничены директорией `PROJECT_ROOT` (env var). Путь, выходящий за её пределы через `../` или абсолютный адрес, блокируется — [tools.py: `_safe_path()`](tools.py).
- **Whitelist команд**: `run_tests` принимает только команды с префиксами `pytest`, `python -m pytest`, `flake8`, `pip check` — [tools.py: `ALLOWED_PREFIXES`](tools.py).
- **Блокировка shell-инъекций**: символы `;`, `&&`, `|`, `>`, `` ` ``, `$(` запрещены в строке команды.
- **Исключение служебных папок**: поиск не заходит в `.venv`, `.git`, `__pycache__` — [tools.py: `SKIP_DIRS`](tools.py).
- **Логи без секретов**: в лог пишутся имя tool, входные параметры и статус; содержимое файлов не логируется.

## Интеграция с Claude Code

1. Клонировать репозиторий и перейти в папку:
   ```powershell
   cd F:\Otus\otus-ai-course\homework-5-mcp
   ```

2. Создать виртуальное окружение и установить зависимости:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

3. Скопировать `.env.example` в `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

4. Открыть папку проекта в Claude Code — файл `.mcp.json` подхватывается автоматически. Сервер `homework-mcp` появится в списке подключённых MCP-серверов.

5. Проверить работу — спросить в чате:
   > "Что такое FastMCP?" → вызовет `tool_get_doc`  
   > "Найди упоминания pytest в проекте" → вызовет `tool_search_files`

## Запуск Inspector (для отладки)

Виртуальное окружение должно быть активно (`(.venv)` в начале строки).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install mcp[cli]
mcp dev server.py
```

Откроется Inspector. Должны появиться все 4 инструмента: `tool_get_doc`, `tool_read_file`, `tool_search_files`, `tool_run_tests`.
