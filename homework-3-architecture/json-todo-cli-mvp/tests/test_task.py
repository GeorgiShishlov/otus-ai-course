# [TODO-MVP]
import pytest
import uuid
from datetime import datetime, timedelta
import re

from core.models import Task

ID_task = uuid.uuid4()


@pytest.fixture
def task_fabric():
    """Фабрика для создания задач с кастомными параметрами"""

    def create_task(
            id_task=None,
            name_task='Тестовая задача',
            created_date=None,
            description_task=None,
            status_task=1,
            due_date=None
    ):
        return {
            'id_task': id_task,
            'name_task': name_task,
            'created_date': created_date,
            'description_task': description_task,
            'status_task': status_task,
            'due_date': due_date
        }

    return create_task


class TestTaskID:
    def test_task_id_uuid_created(self, task_fabric):
        """Задача с корректным ID создается при передаче UUID, тип данных id_task - UUID,
        геттер возвращает корректное текущее значение"""
        id_uuid = uuid.uuid4()
        obj = Task(**task_fabric(id_task=id_uuid))
        assert isinstance(obj, Task)
        assert type(obj.id_task) is uuid.UUID
        assert obj.id_task == id_uuid

    def test_task_id_none_created(self, task_fabric):
        """Задача с корректным ID создается при передаче None, тип данных id_task - UUID,
        геттер возвращает текущее значение"""
        obj = Task(**task_fabric())
        assert isinstance(obj, Task)
        assert type(obj.id_task) is uuid.UUID

    def test_task_id_str_created(self, task_fabric):
        """Задача с корректным ID создается при передаче str, тип данных id_task - UUID,
        геттер возвращает корректное текущее значение"""
        id_uuid = uuid.uuid4()
        id_uuid_str = str(id_uuid)
        obj = Task(**task_fabric(id_task=id_uuid_str))
        assert isinstance(obj, Task)
        assert type(obj.id_task) is uuid.UUID
        assert obj.id_task == id_uuid

    def test_task_id_incorrect_uuid(self, task_fabric):
        """Возникает исключение ValueError при передаче некорректной строки"""
        with pytest.raises(ValueError):
            Task(**task_fabric(id_task='некорректная строка'))
        with pytest.raises(ValueError):
            Task(**task_fabric(id_task=''))

    def test_task_id_incorrect_type_data(self, task_fabric):
        """Возникает исключение TypeError при передаче некорректного типа данных (не uuid.uuid4(), str, None)"""
        with pytest.raises(TypeError):
            Task(**task_fabric(id_task=123))

    def test_task_id_setter_after_creation(self, task_fabric):
        """Проверка изменения id через сеттер после создания"""
        task = Task(**task_fabric())
        original_id = task.id_task

        new_uuid = uuid.uuid4()
        task.id_task = new_uuid

        assert task.id_task == new_uuid
        assert task.id_task != original_id

        # Проверка через строку
        another_uuid = uuid.uuid4()
        task.id_task = str(another_uuid)
        assert task.id_task == another_uuid


class TestTaskName:
    def test_task_name_correct(self, task_fabric):
        """Задача с корректным name_task создается при передаче корректной строки
        (длина 20 - верхняя точка лимита длины), геттер возвращает корректное текущее значение"""
        value = ''.join('a' * 20)
        obj = Task(**task_fabric(name_task=value))
        assert isinstance(obj, Task)
        assert obj.name_task == value

    def test_task_name_not_str(self, task_fabric):
        """Возникает исключение TypeError при передаче некорректного типа данных (str)"""
        with pytest.raises(TypeError):
            Task(**task_fabric(name_task=1))

    def test_task_name_not_empty(self, task_fabric):
        """Возникает исключение TypeError при передаче пустой строки"""
        with pytest.raises(ValueError):
            Task(**task_fabric(name_task=''))

    def test_task_name_len_21(self, task_fabric):
        """Возникает исключение TypeError при передаче строки по длине (21) превышающей лимит длины (20)"""
        with pytest.raises(ValueError):
            Task(**task_fabric(name_task=''.join('a' * 21)))

    def test_task_name_setter_after_creation(self, task_fabric):
        """Проверка изменения name_task через сеттер после создания"""
        task = Task(**task_fabric(name_task=''.join('a' * 20)))
        original_name = task.name_task

        new_str = ''.join([' ', 'b', ' '])
        task.name_task = new_str

        assert task.name_task == new_str.strip()
        assert task.name_task != original_name


class TestTaskCreateDate:
    def test_task_created_date_none_created(self, task_fabric):
        """Задача создается при передаче None, геттер возвращает корректное текущее значение"""
        # Засекаем время ДО создания объекта
        before_creation = datetime.now().replace(second=0, microsecond=0)

        # Создаем объект
        obj = Task(**task_fabric())

        # Засекаем время ПОСЛЕ создания
        after_creation = datetime.now().replace(second=0, microsecond=0)

        assert isinstance(obj, Task)
        assert obj.created_date is not None
        assert isinstance(obj.created_date, datetime)

        # Проверяем, что дата находится в ожидаемом диапазоне
        assert before_creation <= obj.created_date <= after_creation

    def test_task_created_date_datetime_created(self, task_fabric):
        """Задача с корректной датой created_date создается при передаче datetime,
        геттер возвращает корректное текущее значение. Тестирование валидатора _validate_date"""
        created_date_ = datetime.now().replace(second=0, microsecond=0)
        obj = Task(**task_fabric(created_date=created_date_))
        assert isinstance(obj, Task)
        assert obj.created_date == created_date_

    def test_task_created_date_str_created(self, task_fabric):
        """Задача с корректной датой created_date создается при передаче str,
        геттер возвращает корректное текущее значение. Тестирование валидатора _validate_date"""
        created_date_ = "2024-01-15 15:30"
        obj = Task(**task_fabric(created_date=created_date_))
        assert isinstance(obj, Task)
        assert obj.created_date == datetime.strptime(created_date_, '%Y-%m-%d %H:%M')

    def test_task_created_date_incorrect_str(self, task_fabric):
        """Возникает исключение ValueError при передаче некорректной даты в формате строки.
        Тестирование валидатора _validate_date"""
        with pytest.raises(ValueError):
            Task(**task_fabric(created_date='25-10-11 20:00:00'))

    def test_task_created_date_incorrect_type_data(self, task_fabric):
        """Возникает исключение TypeError при передаче некорректного типа данных.
        Тестирование валидатора _validate_date
        С int (не None, str, datetime)"""
        with pytest.raises(TypeError):
            Task(**task_fabric(created_date=2025 - 10 - 11))

    def test_task_created_date_setter_after_creation(self, task_fabric):
        """Проверка изменения created_date через сеттер после создания.
        Тестирование валидатора _validate_date"""
        task = Task(**task_fabric())
        original_created_date = task.created_date

        new_created_date = datetime.now() + timedelta(hours=2)
        task.created_date = new_created_date

        assert task.created_date == new_created_date
        assert task.created_date != original_created_date


class TestTaskDescription:
    def test_task_description_none_created(self, task_fabric):
        """Задача создается при передаче None, геттер возвращает None"""
        obj = Task(**task_fabric())
        assert isinstance(obj, Task)
        assert type(obj.description_task) is type(None)

    def test_task_description_correct(self, task_fabric):
        """Задача с корректным description_task создается при передаче корректной строки
        (длина 300 - верхняя точка лимита длины), геттер возвращает корректное текущее значение"""
        value = ''.join('a' * 300)
        obj = Task(**task_fabric(description_task=value))
        assert isinstance(obj, Task)
        assert obj.description_task == value

    def test_task_description_incorrect_data(self, task_fabric):
        """Возникает исключение TypeError при передаче некорректного типа данных"""
        with pytest.raises(TypeError):
            Task(**task_fabric(description_task=1))

    def test_task_name_len_21(self, task_fabric):
        """Возникает исключение TypeError при передаче строки по длине (301) превышающей лимит длины (300)"""
        with pytest.raises(ValueError):
            Task(**task_fabric(description_task=''.join('a' * 301)))

    def test_task_name_setter_after_creation(self, task_fabric):
        """Проверка изменения description_task через сеттер после создания"""
        task = Task(**task_fabric(description_task=''.join('a' * 300)))
        original_name = task.description_task

        new_str = ''.join([' ', 'b', ' '])
        task.description_task = new_str

        assert task.description_task == new_str.strip()
        assert task.description_task != original_name


class TestTaskStatus:
    def test_task_status_correct_str(self, task_fabric):
        """Задача создается при передаче int, геттер возвращает переданное значение"""
        status_task_ = 1
        obj = Task(**task_fabric(status_task=status_task_))
        assert isinstance(obj, Task)
        assert obj.status_task == status_task_

    def test_task_status_correct_none(self, task_fabric):
        """Возникает исключение TypeError при передаче некорректного типа данных"""
        with pytest.raises(TypeError):
            Task(**task_fabric(status_task=0.5))
        with pytest.raises(TypeError):
            Task(**task_fabric(status_task=True))

    def test_task_status_not_str_none(self, task_fabric):
        """Возникает исключение ValueError при передаче значения не входящего в TASK_STATUSES.keys() (входят 1,2,3,4)"""
        with pytest.raises(ValueError):
            Task(**task_fabric(status_task=0))

    def test_task_status_setter_after_creation(self, task_fabric):
        """Проверка изменения status_task через сеттер после создания"""
        task = Task(**task_fabric(status_task=2))
        original_status = task.status_task

        new_status = 3
        task.status_task = new_status

        assert task.status_task == new_status
        assert task.status_task != original_status


class TestTaskDueDate:
    def test_task_due_data_none_created(self, task_fabric):
        """Задача с корректной датой due_date создается при передаче None,
        геттер возвращает корректное текущее значение"""
        due_date_ = None
        obj = Task(**task_fabric(due_date=due_date_))
        assert isinstance(obj, Task)
        assert obj.due_date == due_date_

    def test_task_due_data_datetime_created(self, task_fabric):
        """Задача с корректной датой due_date создается при передаче datetime,
        геттер возвращает корректное текущее значение. Тестирование валидатора _validate_date"""
        due_date_ = datetime.now().replace(second=0, microsecond=0)
        obj = Task(**task_fabric(due_date=due_date_))
        assert isinstance(obj, Task)
        assert obj.due_date == due_date_

    def test_task_due_data_str_created(self, task_fabric):
        """Задача с корректной датой due_date создается при передаче str,
        геттер возвращает корректное текущее значение. Тестирование валидатора _validate_date"""
        due_date_ = "2024-01-15 15:30"
        obj = Task(**task_fabric(due_date=due_date_))
        assert isinstance(obj, Task)
        assert obj.due_date == datetime.strptime(due_date_, '%Y-%m-%d %H:%M')

    def test_task_due_date_incorrect_str(self, task_fabric):
        """Возникает исключение ValueError при передаче некорректной даты в формате строки.
        Тестирование валидатора _validate_date"""
        with pytest.raises(ValueError):
            Task(**task_fabric(due_date='25-10-11 20:00:00'))

    def test_task_due_date_incorrect_type_data(self, task_fabric):
        """Возникает исключение TypeError при передаче некорректного типа данных.
        Тестирование валидатора _validate_date
        С int (не None, str, datetime)"""
        with pytest.raises(TypeError):
            Task(**task_fabric(due_date=2025 - 10 - 11))

    def test_task_due_date_setter_after_creation(self, task_fabric):
        """Проверка изменения due_date через сеттер после создания.
        Тестирование валидатора _validate_date"""
        task = Task(**task_fabric())
        original_due_date = task.due_date

        new_due_date = datetime.now() + timedelta(hours=2)
        task.due_date = new_due_date

        assert task.due_date == new_due_date
        assert task.due_date != original_due_date


class TestValidateDate:
    def test_validate_date_with_valid_string(self):
        """Тест валидной строки даты"""
        test_date = "2023-12-31 23:59"
        result = Task._validate_date(test_date)
        expected = datetime(2023, 12, 31, 23, 59)
        assert result == expected

    def test_validate_date_with_datetime_object(self):
        """Тест с объектом datetime"""
        test_date = datetime(2023, 12, 31, 23, 59, 0, 0)
        result = Task._validate_date(test_date)
        assert result == test_date

    # Граничные значения дат и времени
    def test_validate_date_string_29_february_leap_year(self):
        """Тест 29 февраля високосного года как строки"""
        result = Task._validate_date("2024-02-29 23:59")
        expected = datetime(2024, 2, 29, 23, 59)
        assert result == expected

    def test_validate_date_string_29_february_non_leap_year(self):
        """Тест 29 февраля НЕвисокосного года как строки - ДОЛЖЕН УПАСТЬ (2023 не високосный)"""
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("2023-02-29 23:59")

    def test_validate_date_string_31_april(self):
        """Тест 30 апреля как строки - ДОЛЖЕН УПАСТЬ (в апреле 30 дней)"""
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("2025-04-31 23:59")

    def test_validate_date_string_month_13(self):
        """Тест 13-ый месяц как строки - ДОЛЖЕН УПАСТЬ (нет 13 ого месяца)"""
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("2025-13-01 12:00")

    def test_validate_date_string_31_december(self):
        """Тест 31 декабря как строки (конец года)"""
        result = Task._validate_date("2024-12-31 23:59")
        expected = datetime(2024, 12, 31, 23, 59)
        assert result == expected

    def test_validate_date_string_1_january(self):
        """Тест 1 января как строки (начало года)"""
        result = Task._validate_date("2025-01-01 00:00")
        expected = datetime(2025, 1, 1, 0, 0)
        assert result == expected

    def test_validate_date_string_24_00(self):
        """Тест 24:00 как строки - ДОЛЖЕН УПАСТЬ (несуществующее время)"""
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("2025-01-05 24:00")

    def test_validate_date_string_23_60(self):
        """Тест 23:60 как строки - ДОЛЖЕН УПАСТЬ (несуществующее время)"""
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("2025-01-05 23:60")

    def test_validate_date_min_date(self):
        """Минимальная поддерживаемая дата"""
        result = Task._validate_date("0001-01-01 00:00")
        expected = datetime(1, 1, 1, 0, 0)
        assert result == expected

    def test_validate_date_max_date(self):
        """Максимальная поддерживаемая дата"""
        result = Task._validate_date("9999-12-31 23:59")
        expected = datetime(9999, 12, 31, 23, 59)
        assert result == expected

    # Неправильные форматы строк
    def test_validate_date_with_invalid_string_format_not_time(self):
        """Тест неверного формата строки (Отсутствие времени - только дата "YYYY-MM-DD")"""
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("2023-12-31")

    def test_validate_date_with_invalid_string_format_incorrect_separator(self):
        """Тест неверного формата строки (Неправильный разделитель)"""
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("2023:12:31 15:40")
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("2023-12-31 15-40")

    def test_validate_date_with_invalid_string_format_reverse_order(self):
        """Тест неверного формата строки (Обратный порядок - "DD-MM-YYYY HH:MM")"""
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("31-12-2023 15:40")

    def test_validate_date_with_invalid_string_format_extra_characters_spaces(self):
        """Тест неверного формата строки (С лишними символами и пробелами -
        пробелы в начале/конце строки, специальные символы)"""
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date(" 2023-12-31 15:40")
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("2023-12-31 15:40 ")
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("/2023-12-31 15:40")
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("   ")
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("\t\t\t")
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date(" \t \n ")

    def test_validate_date_with_invalid_string(self):
        """Тест полностью невалидной строки"""
        with pytest.raises(ValueError, match="Неверный формат даты создания. Ожидается: YYYY-MM-DD HH:MM"):
            Task._validate_date("not-a-date")

    # Некорректные типы данных
    @pytest.mark.parametrize("invalid_input, expected_type", [
        (None, type(None)),
        (123, type(123)),
        (1.23, type(1.23)),
        (True, type(True)),
        ([2025, 2, 1, 12, 0], type([2025, 2, 1, 12, 0])),
        ({'date': '2023-12-31'}, type({'date': '2023-12-31'})),
    ])
    def test_validate_date_with_wrong_type(self, invalid_input, expected_type):
        """Тест неправильного типа данных + Тест сообщений TypeError для различных типов"""
        expected_message = f"Ожидается один из типов {datetime, str}, получен тип {expected_type}"
        with pytest.raises(TypeError, match=re.escape(expected_message)):
            Task._validate_date(invalid_input)

    # Проверка возвращаемых значений
    @pytest.mark.parametrize("test_date_str, expected_datetime", [
        ("2023-12-31 23:59", datetime(2023, 12, 31, 23, 59)),
        ("2024-02-29 12:00", datetime(2024, 2, 29, 12, 0)),
        ("2023-01-01 00:00", datetime(2023, 1, 1, 0, 0))
    ])
    def test_validate_date_exact_match(self, test_date_str, expected_datetime):
        """Тест точного соответствия возвращаемого значения"""
        result = Task._validate_date(test_date_str)

        assert result == expected_datetime
        assert result.year == expected_datetime.year
        assert result.month == expected_datetime.month
        assert result.day == expected_datetime.day
        assert result.hour == expected_datetime.hour
        assert result.minute == expected_datetime.minute

    def test_validate_date_invalid_month_error_contains_value(self):
        """Сообщение ValueError должно содержать невалидное значение (регрессия бага month=13)"""
        bad_value = "2020-13-01 00:00"
        with pytest.raises(ValueError, match=re.escape(bad_value)):
            Task._validate_date(bad_value)

    def test_validate_date_from_string_has_no_extra_precision(self):
        """Тест, что дата из строки не имеет лишней точности"""
        test_date = "2023-12-31 23:59"
        result = Task._validate_date(test_date)

        assert result.second == 0
        assert result.microsecond == 0
        assert hasattr(result, 'second')  # убедимся что атрибут существует
        assert hasattr(result, 'microsecond')


# Интеграционные тесты
def test_complete_task_creation(task_fabric):
    """Тест создания задачи со всеми заполненными полями"""
    complete_data = {
        'id_task': uuid.uuid4(),
        'name_task': 'Полная задача',
        'created_date': '2024-01-15 10:00',
        'description_task': 'Это полное описание задачи',
        'status_task': 2,
        'due_date': '2024-01-20 15:00'
    }

    task = Task(**complete_data)

    assert task.id_task == complete_data['id_task']
    assert task.name_task == complete_data['name_task']
    assert task.created_date == datetime(2024, 1, 15, 10, 0)
    assert task.description_task == complete_data['description_task']
    assert task.status_task == complete_data['status_task']
    assert task.due_date == datetime(2024, 1, 20, 15, 0)


def test_multiple_property_changes(task_fabric):
    """Тест последовательного изменения нескольких свойств"""
    task = Task(**task_fabric())
    original_state = {
        'name': task.name_task,
        'description': task.description_task,
        'status': task.status_task,
        'due_date': task.due_date
    }

    # Первое изменение
    task.name_task = 'Новое название'
    task.status_task = 3

    assert task.name_task == 'Новое название'
    assert task.status_task == 3
    assert task.description_task == original_state['description']
    assert task.due_date == original_state['due_date']

    # Второе изменение
    task.description_task = 'Новое описание'
    new_due_date = datetime.now() + timedelta(days=5)
    task.due_date = new_due_date

    assert task.name_task == 'Новое название'  # Не изменилось
    assert task.status_task == 3  # Не изменилось
    assert task.description_task == 'Новое описание'
    assert task.due_date == new_due_date














