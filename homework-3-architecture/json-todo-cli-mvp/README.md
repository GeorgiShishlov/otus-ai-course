# Console TODO App

A simple console-based TODO application built in Python as an educational project. Focuses on core Python principles, OOP, and test-driven development.

## 🚧 Project Status: Work in Progress

This project is currently under active development as a learning sandbox. Features are being added and refactored regularly. The main goal is educational, not production stability.

## 📖 Learning Objectives & Goals

The primary goal of this project is to practice and solidify core Python and software development skills:

*   **Object-Oriented Programming (OOP):** Designing with classes, inheritance, encapsulation.
*   **Data Persistence:** Using the `json` module to store and load tasks.
*   **Testing:** Writing unit and integration tests with `pytest`.
*   **Software Architecture:** Implementing a simple 3-layer architecture (Presentation, Logic, Data).
*   **Version Control:** Mastering Git workflows with meaningful commits and descriptive messages.
*   **Project Setup:** Managing dependencies with `requirements.txt` and a structured project layout.

## 🛠️ Built With

*   **Language:** Python 3.11
*   **Storage:** JSON (via `json` module)
*   **Testing:** pytest
*   **Version Control:** Git + GitHub

## 📁 Project Structure

```
todo_project/
├── core/
|   ├── __init__.py
|   ├── models.py
|   └── storage.py
└── tests
|   ├── statuses.json
|   ├── task_list.json
|   ├── tasks.json
|   └── users.json
├── requirements.txt
└── README.md
```

## ✨ Current Implementation & Progress
### 🧱 Core Architecture Established:

The project foundation is built around a clear 3-layer architecture:

* **Data Layer:**
  * `JSONStorage`: A dedicated class responsible for all low-level file operations (reading from/writing to JSON). Isolated from business logic.
* **Logic (Business) Layer:**
  * Entities: Pure data classes (`Task`, `User`) that handle their own validation and state management.
  * Managers: Classes (`TaskManager`, `UserManager`) that handle collections of entities (CRUD operations: Create, Read, Update, Delete).
  * Service (in progress): A planned service layer to orchestrate interactions between managers and provide higher-level user workflows.
* **Presentation Layer:**
  * (Planned) The future console-based user interface.

### ✅ Implemented & Tested:

* **`Task` Entity**: Fully implemented and covered with **passing unit tests** (`pytest`). Validates its own data integrity.
* **`User` and `UserManager` classes**: Core implementation is complete (awaiting comprehensive testing).
* **`TaskManager` class**: Core implementation is complete (awaiting comprehensive testing).
* **Persistence**: Basic save/load functionality via the `JSONStorage` class is implemented.

### 🔧 In Immediate Progress (Next Steps):

* **🧪 Testing Phase:** Writing comprehensive unit and integration tests for the `User`, `UserManager`, and `TaskManager` classes to ensure reliability before further development.

* **🛠 Service Layer Development:** Designing and implementing the service class that will act as the main API for the presentation layer, encapsulating the application's core logic.

## 📋 Future Exploration (Ideas):

The feature set is evolving based on the learning process.

