import argparse
import sys
import getpass


def show_main_menu(todo_service):
    """Главное меню"""
    while True:
        print("=" * 50)
        print("Добро пожаловать в \"Мой To-Do List\"")
        print("=" * 50)
        print("Выберите команду")
        print()
        print("Доступные команды:")
        print("1. Зарегистрироваться")
        print("2. Войти")
        print("3. Выйти из программы")
        print("4. Помощь")
        print("=" * 50)

        choice = input("Выберите действие (1-4): ").strip()

        if choice == '1':
            if register_user(todo_service):
                show_user_menu(todo_service)
        elif choice == '2':
            if login_user(todo_service):
                show_user_menu(todo_service)
        elif choice == '3':
            exit_program()
        elif choice == '4':
            show_help()
        else:
            print("Неверный выбор. Попробуйте снова.")

        input("\nНажмите Enter для продолжения...")


def show_password_validation_rules():
    print()
    print("_" * 50)
    print("Правила валидации:\n"
          "- Длина от 8 до 64 символов\n"
          "- Минимум 1 заглавная буква\n"
          "- Минимум 1 строчная буква\n"
          "- Минимум 1 цифра\n"
          "- Минимум 1 специальный символ (@$!%*?&)\n"
          "- Без пробелов\n")
    print("_" * 50)


def register_user(todo_service):
    """Обработка регистрации"""
    show_password_validation_rules()
    username = input("Имя пользователя: ")
    password1 = input("Введите пароль: ")
    password2 = input("Введите пароль повторно: ")

    result = todo_service.register_user(username, password1, password2)
    if result == 0:
        print(f"Пользователь с логином {username} уже существует. Регистрация не завершена")
        return False
    if result == 1:
        print("Пароли не совпадают. Регистрация не завершена")
        return False
    if result == 2:
        print("Посмотрите на правила валидации")
        return False
    if result == 3:
        todo_service.save_users_data()
        todo_service.reload_users_data()
        todo_service.login(username, password1)
        return True


def login_user(todo_service):
    """Обработка входа"""
    username = input("Имя пользователя: ")
    password = getpass.getpass("Пароль: ")

    try:
        result = todo_service.login(username, password)
        if result == 0:
            print(f"Пользователь с логином {username} не существует. Авторизация не пройдена")
            return False
        if result == 1:
            print("Неверный логин или пароль")
            return False
        if result == 2:
            print("Успешный вход в систему")
            return True
        raise ValueError(f"Непредвиденный результат логина: {result}")

    except ValueError as e:
        print(f"Ошибка при авторизации: {e}")
        return False


def exit_program():
    sys.exit(0)


def show_help():
    print("Справка по использованию:")
    print("Для работы с системой используйте следующие команды:")
    print("- register: создание нового аккаунта")
    print("- login: вход в существующий аккаунт")
    print("- exit: завершение работы программы")
    print("- help: показать эту справку")


def show_user_menu(todo_service):
    """Меню профиля пользователя"""
    while True:
        print("=" * 50)
        print("\"Мой To-Do List\"")
        print(f"Здравствуйте {todo_service.username}")
        print("=" * 50)
        print()
        print("Доступные команды:")
        print("1. Показать все задачи")
        print("2. Добавить новую задачу")
        print("3. Сменить статус задачи")
        print("4. Удалить задачу")
        print("5. Сохранить изменения")
        print("6. Изменить пароль")
        print("7. Выйти из профиля")
        print("8. Выйти из программы")
        print("9. Помощь")
        print("10. Удалить текущий аккаунт")
        print("=" * 50)

        choice = input("Выберите действие (1-7): ").strip()

        if choice == '1':
            show_all_tasks(todo_service)
        elif choice == '2':
            add_new_task(todo_service)
        elif choice == '3':
            change_status_task_(todo_service)
        elif choice == '4':
            del_task(todo_service)
        elif choice == '5':
            save_changes(todo_service)
        elif choice == '6':
            change_password(todo_service)
        elif choice == '7':
            if show_menu_save(todo_service, 0):
                return
        elif choice == '8':
            show_menu_save(todo_service, 1)
        elif choice == '9':
            show_help()
        elif choice == '10':
            if delete_user(todo_service):
                return
        else:
            print("Неверный выбор. Попробуйте снова.")

        input("\nНажмите Enter для продолжения...")


def show_all_tasks(todo_service):
    tasks = todo_service.show_all_tasks_by_user()
    if len(tasks) == 0:
        print("У вас пока нет задач")
        return

    print("\n" + "=" * 80)
    print(f"{'№':<3} {'ЗАДАЧА':<20} {'СТАТУС':<12} {'СОЗДАНА':<16} {'СРОК':<16}")
    print("=" * 80)

    task_mapping = {}
    for i, task in enumerate(tasks, 1):
        task_mapping[i] = task.id_task

        due_date = task.due_date.strftime('%d.%m.%Y') if task.due_date else "нет"
        created = task.created_date.strftime('%d.%m.%Y')
        name = task.name_task[:18] + "..." if len(task.name_task) > 20 else task.name_task
        status_text = get_status_text(task.status_task)

        print(f"{i:<3} {name:<20} {status_text:<12} {due_date:<16} {created:<16}")
    todo_service.set_current_task_mapping(task_mapping)
    return


def get_status_text(status_code):
    """Преобразует код статуса в текст"""
    status_map = {
        1: "не начато",
        2: "в процессе",
        3: "завершено",
        4: "отложено"
    }
    return status_map.get(status_code, "неизвестно")


def add_new_task(todo_service):
    """Обработка добавления новой задачи"""
    name_task = input("\nИмя задачи: ")
    description_task = input("Описание задачи (можно оставить пустым): ")
    print_task_statuses()
    status_task = input("Статус задачи: ")
    due_date = input(f"Формат: YYYY-MM-DD HH:MM\n"
                     f"Дата выполнения (можно оставить пустым): ")
    # добавить валидацию данных и ответы об ошибках
    try:
        todo_service.add_task_by_user(name_task=name_task, description_task=description_task,
                                      status_task=status_task, due_date=due_date)

    except Exception as e:
        print(f"Ошибка при создании задачи: {e}")
        return False


def change_status_task_(todo_service):
    """Обработка изменения статуса задачи"""
    show_all_tasks(todo_service)

    task_num = int(input("\nВведите номер задачи для изменения статуса: "))
    task_id = todo_service.get_task_id_by_number(task_num)

    if not task_id:
        print("Неверный номер задачи")
        return

    print_task_statuses()

    new_status = input("Новый статус задачи (1-4): ").strip()

    if new_status not in ['1', '2', '3', '4']:
        print("Неверный статус")
        return

    try:
        todo_service.change_status_task(task_id, int(new_status))
        print("Статус задачи успешно изменен")

    except ValueError:
        print("Ошибка при изменении статуса")


def print_task_statuses():
    print(f"\nДоступные статусы:")
    print("1: не начато")
    print("2: в процессе")
    print("3: завершено")
    print("4: отложено")


def del_task(todo_service):
    """Обработка удаления задачи"""
    show_all_tasks(todo_service)

    task_num = int(input("\nВведите номер задачи для для удаления: "))
    task_id = todo_service.get_task_id_by_number(task_num)

    if not task_id:
        print("Неверный номер задачи")
        return

    decision_del = input(f"Удалить задачу № {task_num}? (y/n): ")
    if decision_del.strip() == 'y':
        try:
            todo_service.delete_task(task_id)
            print("Статус задачи успешно изменен")

        except ValueError:
            print("Ошибка при изменении статуса")
    else:
        return


def save_changes(todo_service):
    """Обработка сохранения изменений"""
    todo_service.save_users_data()
    todo_service.save_tasks_data()


def change_password(todo_service):
    """Обработка изменения пароля"""
    show_password_validation_rules()
    old_password = input("Введите текущий пароль: ")
    new_password = input("Введите новый пароль: ")

    try:
        result = todo_service.change_password(old_password, new_password)
        if result == 0:
            print("Введенный текущий пароль - некоректен")
            return
        if result == 2:
            print("Пароль успешно изменен")
            return
        if result[0] == 1:
            print(f"{result[1]}. Посмотрите на правила валидации")
            return

        raise ValueError(f"Непредвиденный результат при изменении пароля: {result}")

    except ValueError as e:
        print(f"Ошибка при изменении пароля: {e}")
        return


def show_menu_save(todo_service, flag):
    collect = ["профиля", "программы"]
    decision_exit = input(f"Действительно хотите выйти из {collect[flag]}? (y/n) ")
    if decision_exit == 'y':
        decision_save = input("Сохранть изменения? (y/n) ")
        if decision_save == 'y':
            save_changes(todo_service)
        if flag == 0:
            return True
        else:
            exit_program()
    return False


def delete_user(todo_service):
    todo_service.delete_user()
    return True
