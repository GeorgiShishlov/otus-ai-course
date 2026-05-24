# Демо — MCP Server в действии

Все 5 запросов выполнены в чате Claude Code с подключённым `homework-mcp` сервером.
Минимум требований ТЗ: 5 запросов, из них 3+ реально вызывают MCP-tool. Здесь все 5 вызывают tool.

---

## Запрос 1 — Справка по термину (tool_get_doc)

**Запрос:** "Объясни термин Tool"  
**Вызван tool:** `tool_get_doc(term="Tool")`

```json
{
  "term": "Tool",
  "description": "Функция на сервере, которую можно вызвать, имеет имя, описание(которe читает языковая модель, и именно по нему она решает, когда вызывать инструмент), параметы и результат.",
  "error": null
}
```

---

## Запрос 2 — Чтение файла (tool_read_file)

**Запрос:** "Прочитай файл requirements.txt"  
**Вызван tool:** `tool_read_file(path="requirements.txt")`

```json
{
  "path": "requirements.txt",
  "content": "mcp>=1.9.0\npython-dotenv>=1.0.0\npytest>=8.0.0",
  "error": null
}
```

---

## Запрос 3 — Поиск по файлам (tool_search_files)

**Запрос:** "Найди все упоминания FastMCP в проекте"  
**Вызван tool:** `tool_search_files(query="FastMCP")`

```json
{
  "query": "FastMCP",
  "matches": [
    { "file": "docs\\glossary.md", "line": 19, "text": "## FastMCP" },
    { "file": "server.py", "line": 5, "text": "from mcp.server.fastmcp import FastMCP" },
    { "file": "server.py", "line": 20, "text": "mcp = FastMCP(\"homework-mcp\")" },
    { "file": "README.md", "line": 142, "text": "> \"Что такое FastMCP?\" → вызовет `tool_get_doc`" }
  ],
  "error": null
}
```

---

## Запрос 4 — Запуск тестов (tool_run_tests)

**Запрос:** "Запусти тесты проекта"  
**Вызван tool:** `tool_run_tests(command="pytest --version")`

```json
{
  "command": "pytest --version",
  "output": "pytest 9.0.3\n",
  "status": "success",
  "error": null
}
```

---

## Запрос 5 — Справка по термину (tool_get_doc)

**Запрос:** "Объясни что такое stdio в контексте MCP"  
**Вызван tool:** `tool_get_doc(term="stdio")`

```json
{
  "term": "stdio",
  "description": "Используется для локальной работы. Не нужно запускать сервер и общаться в браузере. Один процесс запускает другой процесс и общаются через JSON-RPC. Стандартные потоки stdin и stdout.",
  "error": null
}
```
