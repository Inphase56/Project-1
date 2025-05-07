"""
gui.py - Full-featured PyQt6 Task Tracker GUI.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QLineEdit, QDialog, QDialogButtonBox,
    QMessageBox
)
from PyQt6.QtCore import Qt
from model import Task, TaskManager


class TaskDialog(QDialog):
    def __init__(self, task: Task = None):
        super().__init__()
        self.setWindowTitle("Task")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Task Title")
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_input)

        self.due_date_input = QLineEdit()
        self.due_date_input.setPlaceholderText("e.g. 2025-05-01")
        layout.addWidget(QLabel("Due Date:"))
        layout.addWidget(self.due_date_input)

        self.priority_input = QLineEdit()
        self.priority_input.setPlaceholderText("High / Medium / Low")
        layout.addWidget(QLabel("Priority:"))
        layout.addWidget(self.priority_input)

        if task:
            self.title_input.setText(task.title)
            self.due_date_input.setText(task.due_date)
            self.priority_input.setText(task.priority)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        return {
            "title": self.title_input.text().strip(),
            "due_date": self.due_date_input.text().strip(),
            "priority": self.priority_input.text().strip()
        }


class TaskApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Tracker")
        self.setGeometry(100, 100, 600, 400)
        self.task_manager = TaskManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Task List:")
        layout.addWidget(self.label)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Title", "Due Date", "Priority", "Completed"])
        layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        buttons = [
            ("Add Task", self.add_task),
            ("Edit Task", self.edit_task),
            ("Delete Task", self.delete_task),
            ("Mark Completed", self.mark_completed),
        ]
        for text, handler in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def refresh_table(self):
        self.table.setRowCount(0)
        for task in self.task_manager.get_tasks():
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, val in enumerate(task.to_list()):
                self.table.setItem(row, col, QTableWidgetItem(val))

    def get_selected_task_index(self):
        selected = self.table.currentRow()
        if selected < 0 or selected >= len(self.task_manager.get_tasks()):
            return None
        return selected

    def add_task(self):
        dialog = TaskDialog()
        if dialog.exec():
            data = dialog.get_data()
            if not data["title"]:
                QMessageBox.warning(self, "Input Error", "Task title cannot be empty.")
                return
            task = Task(data["title"], data["due_date"], data["priority"])
            self.task_manager.add_task(task)
            self.refresh_table()

    def edit_task(self):
        index = self.get_selected_task_index()
        if index is None:
            QMessageBox.information(self, "Select Task", "Please select a task to edit.")
            return
        task = self.task_manager.get_tasks()[index]
        dialog = TaskDialog(task)
        if dialog.exec():
            data = dialog.get_data()
            task.title = data["title"]
            task.due_date = data["due_date"]
            task.priority = data["priority"]
            self.refresh_table()

    def delete_task(self):
        index = self.get_selected_task_index()
        if index is None:
            QMessageBox.information(self, "Select Task", "Please select a task to delete.")
            return
        self.task_manager.tasks.pop(index)
        self.refresh_table()

    def mark_completed(self):
        index = self.get_selected_task_index()
        if index is None:
            QMessageBox.information(self, "Select Task", "Please select a task to mark as completed.")
            return
        self.task_manager.tasks[index].completed = True
        self.refresh_table()
