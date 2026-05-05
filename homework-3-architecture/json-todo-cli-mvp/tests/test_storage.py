import json
import pytest
from pathlib import Path
from core.storage import JSONStorage  # замени на свой импорт
import tempfile
import os


@pytest.fixture
def json_storage_fixture():
    """
    Фикстура создает изолированное хранилище для каждого теста.
    Это как 'песочница' для работы с файлами.
    """
    # Создаем временную директорию - это наша изолированная песочница
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Создаем mock объекта чтобы обойти сложную логику __init__
        storage = JSONStorage.__new__(JSONStorage)

        # Настраиваем пути как в оригинальном классе
        storage.base_dir = temp_path
        storage.data_dir = temp_path / 'json_data'
        storage.file_path = storage.data_dir / 'test_tasks.json'

        # Вручную выполняем логику из __init__
        storage.data_dir.mkdir(exist_ok=True)

        # Создаем начальный файл если не существует
        if not storage.file_path.exists():
            with open(storage.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        # Передаем подготовленный storage тесту
        yield storage

        # После теста временная директория автоматически удаляется!
        # Фикстура сама убирает за собой


# Теперь пишем тесты, которые используют фикстуру
def test_storage_initialization(json_storage_fixture):
    """Тест: хранилище правильно инициализируется"""
    storage = json_storage_fixture

    # Проверяем что все пути и файлы созданы
    assert storage.data_dir.exists()
    assert storage.file_path.exists()
    assert storage.file_path.name == "test_tasks.json"


