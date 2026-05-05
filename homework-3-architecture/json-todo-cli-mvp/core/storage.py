import copy
import json
import os
from pathlib import Path

dir_json_data = 'D:/Документы/pet-проекты/todo_list/todo_list/json_data'

names_json_data = ['statuses.json', 'users.json', 'tasks.json', 'task_lists.json']


class JSONStorage:
    """Только для чтения/записи JSON файлов."""

    def __init__(self, filename):
        # Автоматически определяем путь к папке с данными
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / 'json_data'
        self.data_dir.mkdir(exist_ok=True)  # Создаем папку если нет
        self.file_path = self.data_dir / filename

        # Создаем файл с пустым списком если не существует
        if not self.file_path.exists():
            self.save_data([])

    def load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_data(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


class DataFileHandler:  #использую в следующей версии (недоработан, надо все перепроверять и вообще разобраться)
    """Работа с данными JSON файлов"""

    def __init__(self, file_handler: JSONStorage):
        self.__file_handler = file_handler
        self.__data = self.__file_handler.load_data()

    def _commit(self) -> None:
        """Сохранить изменения в файл"""
        self.__file_handler.save_data(self.__data)

    def refresh(self) -> None:
        """Перезагрузить данные из файла"""
        self.__data = self.__file_handler.load_data()

    def get_all(self) -> list[dict]:
        return copy.deepcopy(self.__data)

    def get_by_key(self, key: str) -> list[dict]:
        pass

    def get_dict(self, key_):
        keys_ = self.get_keys()
        if key_ is None or key_ not in keys_:
            return None

