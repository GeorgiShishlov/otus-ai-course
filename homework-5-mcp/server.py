# server.py
import logging
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tools import read_file, search_files, run_tests, get_doc

# Загружаем переменные окружения из .env
load_dotenv()

# Настройка логирования: пишем в stderr (не мешает stdio протоколу)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()]  # по умолчанию stderr
)
log = logging.getLogger("mcp-server")

# Создаём экземпляр MCP-сервера
mcp = FastMCP("homework-mcp")

# ------------------------------------------------------------
# Инструмент 1: получение описания термина из глоссария
# ------------------------------------------------------------
@mcp.tool()
def tool_get_doc(term: str) -> dict:
    """
    Находит определение технического термина в файле docs/glossary.md.
    Аргументы:
        term - искомый термин (регистронезависимо)
    Возвращает словарь с полями:
        term (str) - найденный термин в исходном формате,
        description (str или None) - описание, если найдено,
        error (str или None) - сообщение об ошибке, если термин отсутствует.
    """
    log.info("tool=get_doc term=%r", term)
    result = get_doc(term)
    log.info("tool=get_doc status=%s", "ok" if result["error"] is None else "error")
    return result

# ------------------------------------------------------------
# Инструмент 2: чтение файла по пути (относительно PROJECT_ROOT)
# ------------------------------------------------------------
@mcp.tool()
def tool_read_file(path: str) -> dict:
    """
    Читает содержимое текстового файла.
    Аргументы:
        path - путь к файлу относительно PROJECT_ROOT (или абсолютный).
    Возвращает словарь:
        content (str) - содержимое файла,
        error (str или None) - описание ошибки.
    """
    log.info("tool=read_file path=%s", path)
    result = read_file(path)
    if result.get("error"):
        log.warning("tool=read_file error=%s", result["error"])
    else:
        log.info("tool=read_file size=%d bytes", len(result.get("content", "")))
    return result

# ------------------------------------------------------------
# Инструмент 3: поиск файлов по паттерну
# ------------------------------------------------------------
@mcp.tool()
def tool_search_files(query: str, search_path: str = ".") -> dict:
    """
    Ищет текст внутри файлов проекта (регистронезависимо).
    Аргументы:
        query - строка для поиска внутри содержимого файлов,
        search_path - подпапка поиска (по умолчанию корень проекта).
    Возвращает словарь:
        matches (list) - список совпадений {file, line, text},
        error (str или None).
    """
    log.info("tool=search_files query=%r search_path=%s", query, search_path)
    result = search_files(query, search_path)
    if result.get("error"):
        log.warning("tool=search_files error=%s", result["error"])
    else:
        log.info("tool=search_files found=%d matches", len(result.get("matches", [])))
    return result

# ------------------------------------------------------------
# Инструмент 4: запуск тестов pytest
# ------------------------------------------------------------
@mcp.tool()
def tool_run_tests(command: str = "pytest tests/ -v") -> dict:
    """
    Запускает команду из белого списка: pytest, flake8, pip check.
    Shell-операторы (;, &&, |) заблокированы.
    Аргументы:
        command - команда для запуска, например 'pytest tests/ -v' или 'flake8 .'
    Возвращает словарь:
        output (str) - вывод команды,
        status (str) - 'success', 'failure' или 'error',
        error (str или None).
    """
    log.info("tool=run_tests command=%r", command)
    result = run_tests(command)
    log.info("tool=run_tests status=%s", result.get("status"))
    if result.get("error"):
        log.warning("tool=run_tests error=%s", result["error"])
    return result

# ------------------------------------------------------------
# Точка входа — запуск сервера
# ------------------------------------------------------------
if __name__ == "__main__":
    project_root = os.environ.get("PROJECT_ROOT", "not set")
    log.info("Starting homework-mcp (stdio), PROJECT_ROOT=%s", project_root)
    mcp.run(transport="stdio")