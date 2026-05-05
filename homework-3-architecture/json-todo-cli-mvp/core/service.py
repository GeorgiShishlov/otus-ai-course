from core.models import UserManager, TaskManager
from passlib.hash import bcrypt
from core.storage import JSONStorage
import re
from datetime import datetime


pwd_context = bcrypt.using()


class TodoService:
    def __init__(self, storage_users=None, storage_tasks=None):
        if storage_users is None:
            self.__storage_users = []
        if storage_tasks is None:
            self.__storage_tasks = []
        self.__users_manager = UserManager(storage_users)
        self.__tasks_manager = TaskManager(storage_tasks)
        self.__user_id = None
        self.__username = None
        self.__current_task_mapping = {}

    @property
    def user_id(self):
        return self.__user_id

    @property
    def username(self):
        return self.__username

    @property
    def current_task_mapping(self):
        return self.__current_task_mapping

    def set_current_task_mapping(self, mapping):
        self.__current_task_mapping = mapping

    def get_task_id_by_number(self, task_number):
        """Получить task_id по номеру из текущего сопоставления"""
        return self.__current_task_mapping.get(task_number)

    @staticmethod
    def validate_password(password):
        """
        Валидация пароля для MVP проекта.

        Правила:
        - Длина от 8 до 64 символов
        - Минимум 1 заглавная буква
        - Минимум 1 строчная буква
        - Минимум 1 цифра
        - Минимум 1 специальный символ (@$!%*?&)
        - Без пробелов

        Returns:
            tuple: (bool, str) - (валиден ли пароль, сообщение об ошибке)
        """

        if not password:
            return False, "Пароль не может быть пустым"

        # Проверка длины
        if len(password) < 8:
            return False, "Пароль должен содержать минимум 8 символов"

        if len(password) > 64:
            return False, "Пароль не должен превышать 64 символа"

        # Проверка на пробелы
        if ' ' in password:
            return False, "Пароль не должен содержать пробелы"

        # Проверка на заглавные буквы
        if not re.search('[A-ZА-Я]', password):
            return False, "Пароль должен содержать минимум 1 заглавную букву"

        # Проверка на строчные буквы
        if not re.search('[a-zа-я]', password):
            return False, "Пароль должен содержать минимум 1 строчную букву"

        # Проверка на цифры
        if not re.search('[0-9]', password):
            return False, "Пароль должен содержать минимум 1 цифру"

        # Проверка на специальные символы
        if not re.search('[@$!%*?&]', password):
            return False, "Пароль должен содержать минимум 1 специальный символ (@$!%*?&)"

        return True, "Пароль валиден"

    def save_users_data(self):
        users_data_dict = self.__users_manager.to_dict()
        JSONStorage('users.json').save_data(users_data_dict)

    def save_tasks_data(self):
        task_data_dict = self.__tasks_manager.to_dict()
        JSONStorage('tasks.json').save_data(task_data_dict)

    def reload_users_data(self):
        storage_users = JSONStorage('users.json').load_data()
        self.__users_manager = UserManager(storage_users)

    def reload_tasks_data(self):
        storage_tasks = JSONStorage('tasks.json').load_data()
        self.__tasks_manager = TaskManager(storage_tasks)

    @staticmethod
    def hash_password_passlib(password: str) -> str:
        return pwd_context.hash(password)

    def login(self, username, password):
        """Авторизация пользователя
        :return:
        0 - если логина не существует,
        1 - нет такой пары логин:пароль,
        2 - если все верно, записывает id пользователя в self.__user_id
        """
        if not self.__users_manager.check_login(username):
            return 0
        if not self.__users_manager.check_user_password(username, password):
            return 1
        self.__user_id = self.__users_manager.get_user_id(username)
        self.__username = username
        return 2

    def logout(self):
        self.__user_id = None
        self.__username = None

    def change_password(self, old_password, new_password):
        """Изменение пароля пользователя
        :return: 0 - введенный пользователем текущий пароль не совпадает с паролем в базе.
        1 - если новый пароль не проходит валидацию.
        Меняет пароль, если введенный старый пароль корректен
        """
        flag_valid, ans_valid = self.validate_password(new_password)

        if not self.__users_manager.check_user_password(self.__username, old_password):
            return 0
        elif not flag_valid:
            return 1, ans_valid
        else:
            password_hash = self.hash_password_passlib(new_password)
            self.__users_manager.change_user_password(self.__user_id, password_hash)
            return 2

    def register_user(self, username, password1, password2):
        """Регистрация пользователя
        :return: 0 - если такой логин существует,
        1 - если введенные пароли не совпадают,
        2 - если пароль не проходит валидацию.
        3 - создает пользователя, если логин уникальный и пароли совпадают
        """
        flag_valid, ans_valid = self.validate_password(password1)
        if self.__users_manager.check_login(username):
            return 0
        elif password1 != password2:
            return 1
        elif not flag_valid:
            return 2
        else:
            password_hash = self.hash_password_passlib(password1)
            self.__users_manager.create_user(username, password_hash)
            return 3

    def show_all_tasks_by_user(self):
        task_list_by_user_id = self.__tasks_manager.get_task_list_by_user_id(user_id=self.__user_id)
        print(self.__user_id)
        return task_list_by_user_id

    def add_task_by_user(self, name_task: str, description_task: str = None, status_task: str = '1',
                         due_date: str = None):
        if due_date == "":
            due_date = None
        self.__tasks_manager.create_task(name_task=name_task, user_id=self.__user_id,
                                         description_task=description_task, status_task=int(status_task),
                                         due_date=due_date)

    def change_status_task(self, task_id, new_status):
        self.__tasks_manager.change_status_task(task_id, new_status)

    def change_name_task_by_user(self, user_id, task_id):
        pass

    def change_description_task_by_user(self, user_id, task_id):
        pass

    def change_due_date_task_by_user(self, user_id, task_id):
        pass

    def get_changes(self):
        pass

    def delete_user(self):
        self.__users_manager.delete_user(self.__user_id)
        self.logout()
        self.save_users_data()
        self.reload_users_data()

    def delete_task(self, id_task):
        self.__tasks_manager.delete_task(id_task)
