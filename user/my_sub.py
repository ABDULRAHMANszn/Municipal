import sqlite3
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from db_manager import fetch_user_subscriptions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")


class UserSubscriptions(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Subscriptions for {username}")
        self.resize(900, 500)

        layout = QVBoxLayout(self)
        self.label = QLabel(f"Subscriptions for user: {username}")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.load_data()  # استدعاء التحديث

    def load_data(self):
        # جلب البيانات من الداتا بيز
        data = fetch_user_subscriptions(self.username)

        if data:
            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(data[0]))

            headers = ["Service"] + [f"Field {i}" for i in range(1, len(data[0]))]
            self.table.setHorizontalHeaderLabels(headers)

            for row_idx, row in enumerate(data):
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        else:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.label.setText("No subscriptions found.")
