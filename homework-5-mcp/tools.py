import os
import re
import subprocess
import sys
from pathlib import Path


# ── Sandbox helpers ──────────────────────────────────────────────────────────

def _get_project_root() -> Path:
    """Возвращает корневую папку проекта из env-переменной PROJECT_ROOT.
    Если переменная не задана — папка, где лежит tools.py."""
    root = os.environ.get("PROJECT_ROOT")
    if root is None:
        return Path(__file__).parent.resolve()
    p = Path(root)
    # Относительный путь — отсчитываем от папки tools.py
    if not p.is_absolute():
        p = Path(__file__).parent / p
    return p.resolve()


def _safe_path(relative_path: str) -> Path | None:
    """Разрешает путь внутри PROJECT_ROOT.
    Возвращает None, если путь выходит за пределы корня."""
    root = _get_project_root()
    try:
        target = (root / relative_path).resolve()
        target.relative_to(root)   # ValueError если вышли за пределы
        return target
    except (ValueError, Exception):
        return None


ALLOWED_PREFIXES = ["pytest", "python -m pytest", "flake8", "pip check"]
SHELL_OPERATORS  = [";", "&&", "||", "|", ">", "<", "`", "$("]

# Папки, которые пропускаем при поиске
SKIP_DIRS = {".venv", ".git", "__pycache__", ".pytest_cache", "node_modules"}

def get_doc(term: str) -> dict:
    """
    Ищет определение термина в docs/glossary.md.

    Args:
        term: Искомый термин (регистронезависимо)

    Returns:
        dict: {"term": найденный_термин, "description": текст, "error": None}
              или {"term": term, "description": None, "error": "сообщение"}
    """
    # Путь к файлу глоссария относительно расположения tools.py
    base_dir = Path(__file__).parent
    glossary_path = base_dir / "docs" / "glossary.md"

    try:
        content = glossary_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {
            "term": term,
            "description": None,
            "error": f"Glossary file not found at {glossary_path}"
        }
    except Exception as e:
        return {
            "term": term,
            "description": None,
            "error": f"Failed to read glossary: {e}"
        }
    

    # Шаг 1: найти все заголовки уровня 2 (## Термин) с их позициями
    # Паттерн: начало строки, два решётки, пробел, название термина
    pattern = r'^## (.+)$'
    sections = list(re.finditer(pattern, content, re.MULTILINE))

    # Если нет ни одного заголовка — возвращаем ошибку (хотя файл может быть пуст)
    if not sections:
        return {"term": term, "description": None, "error": "No term entries found in glossary"}

    term_lower = term.lower()

    # Шаг 2: перебираем секции, используя индекс i и сам match
    for i, match in enumerate(sections):
        found_term = match.group(1).strip()
        if found_term.lower() == term_lower:
            # Начало описания: сразу после конца строки заголовка
            start = match.end()
            # Конец описания: начало следующего заголовка или конец файла
            if i + 1 < len(sections):
                end = sections[i + 1].start()
            else:
                end = len(content)
            # Извлекаем и очищаем описание
            description = content[start:end].strip()
            return {"term": found_term, "description": description, "error": None}

    # Если термин не найден
    return {"term": term, "description": None, "error": f"Term '{term}' not found"}


def read_file(path: str) -> dict:
    """Читает файл из папки проекта (ограничено PROJECT_ROOT).

    Args:
        path: Относительный путь к файлу, например 'README.md' или 'src/main.py'
    """
    target = _safe_path(path)
    if target is None:
        return {"path": path, "content": None,
                "error": "Access denied: path escapes PROJECT_ROOT"}
    if not target.exists():
        return {"path": path, "content": None, "error": f"File not found: {path}"}
    if not target.is_file():
        return {"path": path, "content": None, "error": f"Not a file: {path}"}
    try:
        return {"path": path, "content": target.read_text(encoding="utf-8"), "error": None}
    except Exception as e:
        return {"path": path, "content": None, "error": str(e)}


def search_files(query: str, search_path: str = ".") -> dict:
    """Ищет текст в файлах проекта (регистронезависимо, ограничено PROJECT_ROOT).

    Args:
        query:       Текст для поиска
        search_path: Подпапка для поиска (по умолчанию — корень проекта)
    """
    target_dir = _safe_path(search_path)
    if target_dir is None:
        return {"query": query, "matches": None,
                "error": "Access denied: path escapes PROJECT_ROOT"}
    if not target_dir.exists():
        return {"query": query, "matches": None,
                "error": f"Directory not found: {search_path}"}
    matches = []
    try:
        for file_path in sorted(target_dir.rglob("*")):
            # Пропускаем служебные папки
            if any(part in SKIP_DIRS for part in file_path.parts):
                continue
            if not file_path.is_file():
                continue
            # Пропускаем бинарные файлы по расширению
            if file_path.suffix in {".pyc", ".pyo", ".exe", ".dll", ".so"}:
                continue
            try:
                lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
                for line_no, line in enumerate(lines, start=1):
                    if query.lower() in line.lower():
                        rel = str(file_path.relative_to(_get_project_root()))
                        matches.append({"file": rel, "line": line_no, "text": line.strip()})
            except Exception:
                pass  # пропускаем бинарные или недоступные файлы
        return {"query": query, "matches": matches, "error": None}
    except Exception as e:
        return {"query": query, "matches": None, "error": str(e)}


def run_tests(command: str) -> dict:
    """Запускает команду из белого списка в папке проекта.

    Разрешены: pytest, python -m pytest, flake8, pip check.
    Shell-операторы (;, &&, | и др.) заблокированы.

    Args:
        command: Команда для запуска, например 'pytest tests/ -v'
    """
    cmd = command.strip()
    # Блокируем shell-инъекции
    if any(op in cmd for op in SHELL_OPERATORS):
        return {"command": command, "output": None, "status": "error",
                "error": "Shell operators are not allowed"}
    # Проверяем белый список
    if not any(cmd.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        return {"command": command, "output": None, "status": "error",
                "error": f"Command not allowed. Allowed: {ALLOWED_PREFIXES}"}
    # Заменяем 'pytest'/'flake8' на 'python -m pytest'/'python -m flake8'
    # чтобы всегда использовался правильный интерпретатор из текущего окружения
    py = sys.executable
    if cmd.startswith("pytest"):
        args = [py, "-m", "pytest"] + cmd[len("pytest"):].split()
    elif cmd.startswith("python -m pytest"):
        args = [py, "-m", "pytest"] + cmd[len("python -m pytest"):].split()
    elif cmd.startswith("flake8"):
        args = [py, "-m", "flake8"] + cmd[len("flake8"):].split()
    elif cmd.startswith("pip check"):
        args = [py, "-m", "pip", "check"]
    else:
        args = cmd.split()

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            stdin=subprocess.DEVNULL,  # не наследуем stdin от MCP-сервера
            text=True,
            timeout=30,
            cwd=_get_project_root(),
        )
        output = result.stdout + result.stderr
        status = "success" if result.returncode == 0 else "failure"
        return {"command": command, "output": output, "status": status, "error": None}
    except subprocess.TimeoutExpired:
        return {"command": command, "output": None, "status": "error",
                "error": "Timed out after 60s"}
    except Exception as e:
        return {"command": command, "output": None, "status": "error", "error": str(e)}