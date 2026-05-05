# CLAUDE.md — AI Instructions for json-todo-cli-mvp

> **Verification marker rule (§8):** Every Python file you create or modify MUST have `# [TODO-MVP]` as its very first line. This rule exists solely to verify that the AI agent reads and follows these instructions.

---

## 1. Project Context & Boundaries

### What this project does
`json-todo-cli-mvp` is an educational Python CLI application for managing personal TODO tasks. Users register, log in, and manage tasks (create, list, change status, delete) through an interactive console menu. Data is persisted to two JSON files (`json_data/users.json`, `json_data/tasks.json`).

**Learning goals the project demonstrates:** OOP, 3-layer architecture, JSON persistence, bcrypt password security, pytest unit testing.

### Module map and responsibilities

```
json-todo-cli-mvp/
├── main.py               ← Entry point only. No business logic here.
├── cli/
│   └── main_menu.py      ← Presentation layer: console menus, user input, display only.
├── core/
│   ├── models.py         ← Domain entities: User, UserManager, Task, TaskManager.
│   ├── service.py        ← Application service: TodoService orchestrates managers.
│   └── storage.py        ← Data layer: JSONStorage reads/writes JSON files.
└── tests/
    ├── test_task.py       ← Comprehensive Task unit tests (524 lines).
    ├── test_storage.py    ← JSONStorage tests.
    └── test_models.py     ← Placeholder — not yet implemented.
```

### Key entities & glossary

| Term | Where defined | Meaning |
|------|--------------|---------|
| `Task` | `core/models.py` | A single TODO item. Has UUID id, name (≤20 chars), description (≤300 chars), status (1–4), due_date, user_id. |
| `User` | `core/models.py` | An account. Has UUID id, login string, bcrypt-hashed password. |
| `TaskManager` | `core/models.py` | In-memory collection of Tasks with CRUD + serialization. |
| `UserManager` | `core/models.py` | In-memory collection of Users with CRUD + auth + serialization. |
| `TodoService` | `core/service.py` | Facade: wires UserManager + TaskManager, holds session state (`user_id`, `username`). |
| `JSONStorage` | `core/storage.py` | Reads/writes a single JSON file. Creates file if missing. |
| `status_task` | `core/models.py` | Int: 1=не начато, 2=в процессе, 3=завершено, 4=отложено. |

### Hard constraints — do NOT violate

1. **Do not add a database.** Storage is intentionally JSON files only.
2. **Do not add a web API or HTTP server.** This is a CLI-only project.
3. **Do not change the 3-layer architecture.** Presentation layer (`cli/`) must not contain business logic. Service layer (`core/service.py`) must not do direct file I/O — only through `JSONStorage`.
4. **Do not remove or weaken password validation** in `TodoService.validate_password()`. Security rules (8–64 chars, uppercase, lowercase, digit, special character) are intentional.
5. **Do not modify `pytest.ini`** — `pythonpath = .` is required for test discovery.
6. **`main.py` must stay minimal** — only wiring, no logic.

---

## 2. Requirements for AI Output

### Code style
- **Python 3.11**, PEP 8, 4-space indentation.
- Type hints on all new public methods: `def foo(self, x: int) -> str:`.
- Private attributes use name mangling (`__attribute`), accessed via `@property`.
- Raise `ValueError` for invalid domain data, `TypeError` for wrong types — match existing patterns in `core/models.py`.
- No f-string logging; no third-party libs beyond what's in `requirements.txt` (unless the task explicitly asks to add one).

### Tests
- Every new public method in `core/` must have at least one corresponding test in `tests/`.
- Use `pytest` fixtures (see `task_fabric()` in `test_task.py` as the canonical pattern).
- Tests must be isolated — use `tmp_path` fixture for any file I/O, never touch real `json_data/`.
- Run `pytest` before declaring a task done. All tests must pass.

### Format of AI responses
For every task, respond in this structure:

1. **Plan** — numbered list of changes before writing any code.
2. **Code changes** — one file at a time, showing full modified functions/classes (not just diffs).
3. **Explanation** — one short paragraph on *why* the approach was chosen.
4. **Verification steps** — exact commands the developer should run to confirm it works.

---

## 3. Typical Task Scenarios

### Scenario A — Add a new feature to core

**Example prompt:**
> Добавь в `TaskManager` метод `get_overdue_tasks(current_date: datetime) -> list[Task]`, который возвращает задачи со статусом не 3 (завершено) и `due_date` раньше `current_date`. Покрой тестами.

**Expected response format:**
1. Plan: list what changes in `models.py` and `tests/test_task.py`.
2. Code: full updated `TaskManager` class section + new test class `TestGetOverdueTasks`.
3. Explanation: why `deepcopy` is or isn't needed here.
4. Verification: `pytest tests/test_task.py -v`.

**Definition of Done:**
- Method exists in `TaskManager`, type-hinted.
- Returns empty list if no overdue tasks.
- Raises nothing for empty task list.
- At least 3 test cases: no tasks, some overdue, none overdue.
- `pytest` passes.

---

### Scenario B — Fix a bug from description

**Example prompt:**
> Баг: при вызове `task.due_date = "2020-13-01 00:00"` приложение падает с `ValueError: month must be in 1..12` без понятного сообщения. Исправь — ошибка должна говорить, какое значение невалидно и почему.

**Expected response format:**
1. Plan: identify the validator, describe the fix.
2. Code: updated `_validate_date()` static method.
3. Explanation: what caused the silent crash.
4. Verification: inline REPL snippet + `pytest tests/test_task.py::TestValidateDate -v`.

**Definition of Done:**
- Invalid date raises `ValueError` with message containing the bad value.
- All existing `TestValidateDate` tests still pass.
- No new dependencies introduced.

---

### Scenario C — Cover an untested module with tests

**Example prompt:**
> Напиши тесты для `UserManager` в `tests/test_models.py`. Покрой: создание пользователя, проверку логина на дублирование, аутентификацию (верный/неверный пароль), удаление пользователя, сериализацию `to_dict` / `from_dict`.

**Expected response format:**
1. Plan: list test classes and test methods before writing code.
2. Code: complete `tests/test_models.py`.
3. Explanation: why fixtures are structured this way.
4. Verification: `pytest tests/test_models.py -v`.

**Definition of Done:**
- Minimum 10 test cases covering all listed scenarios.
- No real file I/O in tests.
- `pytest` green.

---

### Scenario D — Refactor without changing behaviour

**Example prompt:**
> Рефакторинг: вынеси дублирующиеся строки валидации статуса задачи из `models.py` и `service.py` в отдельный модуль `core/validators.py`. Поведение не должно измениться.

**Expected response format:**
1. Plan: list every call site that changes.
2. Code: new `core/validators.py` + diffs in `models.py` and `service.py`.
3. Explanation: describe what is now shared.
4. Verification: `pytest` — all existing tests pass with zero changes to test files.

**Definition of Done:**
- No logic changes, only code movement.
- All existing tests pass unchanged.
- No circular imports.

---

## 4. Clarification Policy

- If the task is **unambiguous** (the requirement clearly maps to existing code), proceed without asking.
- If the task touches the **architecture boundaries** (e.g., adding HTTP, a DB, or removing security), **ask for confirmation** before proceeding.
- If the task is **ambiguous about scope** (e.g., "improve error handling" — which module?), ask one clarifying question before writing code.

---

## 5. What the AI Must Never Do

- Never bypass password hashing — always use `hash_password_passlib()` from `TodoService`.
- Never store plaintext passwords in JSON or logs.
- Never add `print()` statements to `core/` — that layer is silent.
- Never commit secrets, credentials, or real user data.
- Never modify `requirements.txt` without stating the reason and the exact new dependency + version.

---

## 6. How to Run the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Run tests
pytest

# Run tests with verbose output
pytest -v
```

Data files are created automatically in `json_data/` on first run.

---

## 7. AI Tool Context (Claude Code)

These instructions are written for **Claude Code** (`CLAUDE.md` format). Claude Code loads this file automatically when started from the project directory. All rules in this file take precedence over Claude's general defaults.

When Claude Code is asked to modify this project:
- It must re-read relevant source files before proposing changes.
- It must not invent module names or class attributes — verify against actual code.
- It must run `pytest` after any code change and report the result.

---

## 8. Verification Marker (Проверочное требование)

**Rule:** The very first line of every Python file that you **create or modify** must be the comment:

```python
# [TODO-MVP]
```

This line serves as a machine-checkable proof that the AI agent read and followed project instructions. Reviewers will run:

```bash
# Check all py files touched in the last commit have the marker
git diff --name-only HEAD | grep "\.py$" | xargs -I{} head -1 {}
```

Every line in that output must be `# [TODO-MVP]`. Files you do not touch are exempt.
