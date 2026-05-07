# [TODO-MVP]
TASK_STATUSES = {
    1: "не начато",
    2: "в процессе",
    3: "завершено",
    4: "отложено"
}


def validate_status(value: int) -> None:
    if type(value) is not int:
        raise TypeError(f"Статус должен быть int {TASK_STATUSES.keys()}")
    if value not in TASK_STATUSES:
        raise ValueError(f"Неверный статус задачи. Допустимые значения: {TASK_STATUSES.keys()}")
