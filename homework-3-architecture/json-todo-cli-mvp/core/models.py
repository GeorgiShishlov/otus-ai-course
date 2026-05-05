import copy
import uuid
from datetime import datetime
from passlib.hash import bcrypt

pwd_context = bcrypt.using()

TASK_STATUSES = {
    1: "не начато",
    2: "в процессе",
    3: "завершено",
    4: "отложено"
}


class User:
    def __init__(self, user_id, login, password: list):
        self.__user_id = user_id
        self.__login = login
        self.__password = password

    @property
    def user_id(self) -> 'uuid':
        return self.__user_id

    @property
    def login(self) -> str:
        return self.__login

    @property
    def password(self) -> list:
        return self.__password

    # Методы для работы с паролем (инкапсуляция!)
    def change_password(self, new_password: str) -> None:
        """Изменение пароля"""
        self.__password = new_password

    def check_password(self, password: str) -> bool:
        """Проверка пароля (без раскрытия самого пароля)"""
        return pwd_context.verify(password, self.__password)


class UserManager:
    def __init__(self, storage):
        self.user_list = self.from_dict(storage)

    def create_user(self, name, password): #валидация
        new_user = User(uuid.uuid4(), name, password)
        self.user_list[new_user. user_id] = new_user
        return new_user

    def __get_user_list_by_id(self):
        return copy.deepcopy(self.user_list)

    def __get_user_by_login(self, username):
        users_list = list(filter(lambda user: user.login == username, self.user_list.values()))
        if len(users_list) > 1:
            # Нарушение уникальности логина - это критическая ошибка данных.
            raise KeyError(f"Найдено более одного пользователя с логином '{username}'. Нарушение уникальности логинов.")
        if len(users_list) == 0:
            # Пользователь не найден - ошибка в переданном значении.
            raise ValueError(f"Пользователь с логином '{username}' не найден.")
        if len(users_list) == 1:
            return users_list[0]

    def check_login(self, username):
        """Проверяет существует ли пользователь с таким логином
        :return: True если логин существует, False если такого логина не существует
        """
        users_by_login = [user.login for user in self.user_list.values()]
        if username in users_by_login:
            return True
        return False

    def check_user_password(self, username, password):
        """Сверяет логин и пароль, переданные от TodoService"""
        user = self.__get_user_by_login(username)
        return user.check_password(password)

    def change_user_password(self, user_id, new_password):
        """Изменение пароля пользователя по id пользователя"""
        user = self.user_list[user_id]
        user.change_password(new_password)

    def get_user_id(self, username):
        """Возвращает id пользователя по переданному username"""
        user = self.__get_user_by_login(username)
        return user.user_id

    def delete_user(self, user_id):
        """Удаляет пользователь (НЕДОПИСАН)"""
        if user_id in self.user_list:
            del self.user_list[user_id]
        else:
            raise ValueError(f"User with id {user_id} not found")

    # Сериализация (py -> json)
    def to_dict(self) -> list:
        """Сериализация в словарь для хранения"""
        obj_json = [{
            'id': str(user_v.user_id),
            'login': user_v.login,
            'password': user_v.password,
        }
            for user_v in self.user_list.values()
        ]
        return obj_json

    # Статический метод для десериализации (json -> py) из словаря (от Storage)
    @staticmethod
    def from_dict(data: list) -> dict:
        obj_py = {uuid.UUID(item['id']): User(
            uuid.UUID(item['id']),
            item['login'],
            item['password']
        )
            for item in data
        }
        return obj_py


class Task:
    MAX_NAME_LENGTH = 20
    MAX_DESCRIPTION_LENGTH = 300

    def __init__(self, name_task, user_id, id_task=None, created_date=None, description_task=None, status_task=1, due_date=None):
        self.id_task = id_task
        self.name_task = name_task
        self.created_date = created_date
        self.description_task = description_task
        self.status_task = status_task
        self.due_date = due_date
        self.user_id = user_id

    @staticmethod
    def _validate_date(value: (datetime, str)) -> datetime:
        """Валидирует дату и возвращает datetime объект
        :param value: дата для валидации в формате 'YYYY-MM-DD HH:MM', строка в формате '%Y-%m-%d %H:%M' или None
        :return: datetime объект
        :raises ValueError: если неверный формат строки
        :raises TypeError: если неправильный тип
        """

        if type(value) is str:
            try:
                datetime.strptime(value, '%Y-%m-%d %H:%M')
            except ValueError:
                raise ValueError("Неверный формат даты. Ожидается: YYYY-MM-DD HH:MM")
            return datetime.strptime(value, '%Y-%m-%d %H:%M')

        if type(value) is datetime:
            return value

        raise TypeError(f"Ожидается один из типов {datetime, str}, получен тип {type(value)}")

    @property
    def id_task(self) -> 'uuid':
        return self.__id_task

    @id_task.setter
    def id_task(self, value: (uuid.uuid4(), str, None)) -> uuid.uuid4():
        if value is None:
            self.__id_task = uuid.uuid4()
        elif isinstance(value, uuid.UUID):
            self.__id_task = value
        elif isinstance(value, str):
            try:
                self.__id_task = uuid.UUID(value)
            except ValueError:
                raise ValueError(f"Недопустимая строка UUID: {value}")
        else:
            raise TypeError(f"Ожидается UUID, string или None, получено {type(value)}")

    @property
    def name_task(self) -> str:
        return self.__name_task

    @name_task.setter
    def name_task(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Название должно быть строкой")

        if len(value.strip()) == 0:
            raise ValueError("Название не может быть пустым")

        if len(value.strip()) > self.MAX_NAME_LENGTH:
            raise ValueError(f"Название не может превышать {self.MAX_NAME_LENGTH} символов. Получено: {len(value.strip())}")
        self.__name_task = value.strip()

    @property
    def created_date(self) -> datetime:
        return self.__created_date

    @created_date.setter
    def created_date(self, value: (datetime, str, None)):
        """Устанавливает дату создания. Если None - устанавливает текущую дату"""
        if value is None:
            self.__created_date = datetime.now().replace(second=0, microsecond=0)
        else:
            self.__created_date = self._validate_date(value)

    @property
    def description_task(self) -> str:
        return self.__description_task

    @description_task.setter
    def description_task(self, value: (str, None)):
        if type(value) is not type(None):
            if not isinstance(value, str):
                raise TypeError("Описание должно быть строкой или None")

            if len(value.strip()) > self.MAX_DESCRIPTION_LENGTH:
                raise ValueError(f"Описание не может превышать {self.MAX_DESCRIPTION_LENGTH} символов. Получено: {len(value)}")

            self.__description_task = value.strip()
        else:
            self.__description_task = value

    @property
    def status_task(self) -> int:
        return self.__status_task

    @status_task.setter
    def status_task(self, value: int):
        if type(value) is not int:
            raise TypeError(f"Статус должен быть int {TASK_STATUSES.keys()}")

        if value not in TASK_STATUSES.keys():
            raise ValueError(f"Неверный статус задачи. Допустимые значения: {TASK_STATUSES.keys()}")
        self.__status_task = value

    @property
    def due_date(self) -> datetime:
        return self.__due_date

    @due_date.setter
    def due_date(self, value: (datetime, str, None)):
        if value is None:
            self.__due_date = None
        else:
            self.__due_date = self._validate_date(value)


class TaskManager:
    def __init__(self, storage):
        self.task_list = self.from_dict(storage)

    def create_task(self, name_task: str, user_id: uuid.UUID,
                    description_task: str = None, status_task: int = 1, due_date: datetime = None):
        new_task = Task(
            name_task=name_task,
            user_id=user_id,
            description_task=description_task,
            status_task=status_task,
            due_date=due_date)
        self.task_list[new_task.id_task] = new_task
        return new_task

    def get_task_list(self):
        return copy.deepcopy(self.task_list)

    def get_task_list_by_user_id(self, user_id: uuid.UUID):
        task_list_by_user_id = list(filter(lambda task: task.user_id == user_id, self.task_list.values()))
        return task_list_by_user_id

    def change_status_task(self, task_id: uuid.UUID, new_status: int):
        self.task_list[task_id].status_task = new_status

    def delete_task(self, task_id):
        if task_id in self.task_list:
            del self.task_list[task_id]
        else:
            raise ValueError(f"Task with id {task_id} not found")

    def to_dict(self) -> list:
        """Сериализация в словарь для передачи в JSONStorage (py -> json)"""
        obj_json = [
            {
                'id': str(task_v.id_task),
                'title': task_v.name_task,
                'created_date': task_v.created_date.strftime('%Y-%m-%d %H:%M'),
                'description': task_v.description_task,
                'status': task_v.status_task,
                'due_date': task_v.due_date.strftime('%Y-%m-%d %H:%M') if task_v.due_date is not None else None,
                'user_id': str(task_v.user_id)
            }
            for task_v in self.task_list.values()
        ]
        return obj_json

    @staticmethod
    def from_dict(data: list) -> dict:
        """Статический метод для десериализации (json -> py) из словаря (от Storage)"""
        obj_py = {uuid.UUID(item['id']): Task(
            id_task=uuid.UUID(item['id']),
            name_task=item['title'],
            created_date=datetime.strptime(item['created_date'], '%Y-%m-%d %H:%M'),
            description_task=item['description'],
            status_task=item['status'],
            due_date=item['due_date'],
            user_id=uuid.UUID(item['user_id'])
        )
            for item in data}
        return obj_py


class TodoService:
    def __init__(self):
        pass
