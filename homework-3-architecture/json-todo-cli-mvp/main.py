import sys
from cli.main_menu import show_main_menu
from core.storage import JSONStorage
from core.service import TodoService


def main():
    if len(sys.argv) > 1:
        print("Эта программа работает только в интерактивном режиме.")
        print("Запускайте просто: python todo.py")
        sys.exit(1)

    storage_users = JSONStorage('users.json').load_data()
    storage_tasks = JSONStorage('tasks.json').load_data()

    todo_service = TodoService(storage_users=storage_users, storage_tasks=storage_tasks)

    show_main_menu(todo_service)


if __name__ == "__main__":
    main()

