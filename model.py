"""
model.py - Task model and task manager logic.
"""

from typing import List

class Task:
    def __init__(self, title: str, due_date: str, priority: str, completed: bool = False):
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.completed = completed

    def to_list(self) -> List[str]:
        return [self.title, self.due_date, self.priority, "Yes" if self.completed else "No"]

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks
