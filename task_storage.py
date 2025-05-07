"""
task_storage.py - (Optional) Save/load tasks to/from a CSV file.
"""

import csv
from model import Task

def save_tasks(filename: str, tasks: list[Task]) -> None:
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Due Date", "Priority", "Completed"])
        for task in tasks:
            writer.writerow(task.to_list())
