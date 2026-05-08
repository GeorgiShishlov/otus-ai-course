workspace "json-todo-cli-mvp" "Учебное Python CLI для управления TODO задачами. 3-слойная архитектура." {

    model {

        user = person "Пользователь" "Запускает приложение из терминала, работает с консольным меню"

        todoSystem = softwareSystem "Console TODO App" "Python CLI для регистрации, аутентификации и управления персональными задачами. Данные хранятся в JSON-файлах на диске." {

            consoleApp = container "Console App" "Python-процесс: принимает ввод, выполняет бизнес-логику, сохраняет данные" "Python 3.11" {

                cliLayer = component "CLI / Main Menu" "Слой представления. Консольные меню, ввод и вывод. Не содержит бизнес-логики." "cli/main_menu.py"

                todoService = component "TodoService" "Сервисный слой — фасад. Оркестрирует UserManager и TaskManager. Хранит состояние сессии (user_id, username). Валидация пароля." "core/service.py"

                userManager = component "UserManager" "Коллекция User-объектов в памяти. CRUD + аутентификация через bcrypt. Сериализация to_dict / from_dict." "core/models.py"

                taskManager = component "TaskManager" "Коллекция Task-объектов в памяти. CRUD + фильтрация по user_id. Сериализация to_dict / from_dict." "core/models.py"

                entities = component "Task / User Entities" "Доменные сущности с валидацией через @property-сеттеры. Task: UUID, name ≤20 chars, status 1-4, due_date, user_id. User: UUID, login, bcrypt-hash." "core/models.py"

                validators = component "Validators" "Разделяемая валидация статусов. TASK_STATUSES {1-4} + validate_status(value: int). Не зависит от других модулей." "core/validators.py"

                jsonStorage = component "JSONStorage" "Слой данных. Читает и записывает один JSON-файл. Создаёт файл и директорию json_data/ если отсутствуют." "core/storage.py"

                # --- Связи между компонентами ---
                cliLayer -> todoService "Вызывает методы сервиса" "Python method calls"
                todoService -> userManager "Управляет пользователями"
                todoService -> taskManager "Управляет задачами"
                todoService -> jsonStorage "Загружает и сохраняет данные"
                userManager -> entities "Создаёт и хранит объекты User"
                taskManager -> entities "Создаёт и хранит объекты Task"
                entities -> validators "Task.status_task setter вызывает validate_status()"
            }

            jsonFiles = container "JSON Files" "Постоянное хранилище на диске. Два файла создаются автоматически при первом запуске." "JSON / Filesystem" {
                tags "Database"

                usersJson = component "users.json" "Массив объектов: {id, login, password}. Пароль хранится как bcrypt-хэш." "json_data/users.json"
                tasksJson = component "tasks.json" "Массив объектов: {id, title, description, status, due_date, created_date, user_id}." "json_data/tasks.json"
            }

            # --- Связи между контейнерами ---
            jsonStorage -> usersJson "Читает / записывает" "File I/O"
            jsonStorage -> tasksJson "Читает / записывает" "File I/O"
        }

        # --- Системный контекст ---
        user -> todoSystem "Запускает python main.py, работает через консольное меню"
    }

    views {

        # Уровень 1 — Системный контекст
        systemContext todoSystem "L1_SystemContext" "Уровень 1: Системный контекст" {
            include *
            autoLayout
        }

        # Уровень 2 — Контейнеры
        container todoSystem "L2_Containers" "Уровень 2: Контейнеры" {
            include *
            autoLayout
        }

        # Уровень 3 — Компоненты: Console App
        component consoleApp "L3_Components_App" "Уровень 3: Компоненты Console App" {
            include *
            include jsonFiles
            autoLayout
        }

        # Уровень 3 — Компоненты: JSON Files
        component jsonFiles "L3_Components_JSON" "Уровень 3: Компоненты JSON Files" {
            include *
            autoLayout
        }

        # --- Стили ---
        styles {
            element "Person" {
                shape Person
                background #08427B
                color #ffffff
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "Container" {
                background #438DD5
                color #ffffff
            }
            element "Component" {
                background #85BBF0
                color #000000
            }
            element "Database" {
                shape Cylinder
                background #438DD5
                color #ffffff
            }
        }
    }
}
