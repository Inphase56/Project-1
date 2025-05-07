"""
main.py - Entry point for the Task Tracker application.
"""

from gui import TaskApp

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = TaskApp()
    window.show()
    sys.exit(app.exec())
