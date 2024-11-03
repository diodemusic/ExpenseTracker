import json
import os


PATH = "database.json"


def check_if_json_exists() -> None:
    """
    Checks if a JSON file exists at the specified PATH.
    If the file does not exist or is not readable, creates a new JSON file with an empty "tasks" array.

    :return: None
    """
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        pass
    else:
        with open(PATH, "w") as tasks_json:
            tasks_json.write(json.dumps({"expenses": [], "last_id": 0}))


def load_database() -> dict:
    with open("database.json", "r") as f:
        return json.load(f)


def add_entry(data: dict) -> int:
    database = load_database()

    database["last_id"] += 1
    expense_id = database["last_id"]

    data["expense_id"] = expense_id

    database["expenses"].append(data)

    with open("database.json", "w") as f:
        json.dump(database, f, indent=4)

    return expense_id


def update_database(database: dict) -> None:
    with open("database.json", "w") as f:
        json.dump(database, f, indent=4)


def delete_entry(expense_id: int) -> None:
    expenses = load_database()
    expenses["expenses"].pop(expense_id - 1)

    i = 1
    for expense in expenses["expenses"]:
        expense["expense_id"] = i
        i += 1

    expenses["last_id"] = i - 1

    update_database(expenses)


check_if_json_exists()
