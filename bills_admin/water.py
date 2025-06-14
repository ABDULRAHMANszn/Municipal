import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QApplication
from PyQt5.QtGui import QFont
from db_manager import get_user_id, add_water_bill, create_tables, get_all_usernames


class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel - Water Bills")
        self.setGeometry(700, 250, 500, 600)
        self.setStyleSheet("background-color: #f1f2f6;")
        create_tables()
        self.setup_ui()

    def setup_ui(self):
        font = QFont("Segoe UI", 20)

        # Username Label
        self.userl = QLabel("Username:", self)
        self.userl.setGeometry(20, 20, 200, 50)
        self.userl.setFont(font)

        # Username ComboBox (filled dynamically)
        self.users = QComboBox(self)
        self.users.setGeometry(190, 25, 250, 50)
        self.users.setFont(QFont("Segoe UI", 12))
        self.users.addItems(get_all_usernames())
        self.users.setStyleSheet("background-color: white;")

        # Month Label
        self.months = QLabel("Month:", self)
        self.months.setGeometry(20, 90, 200, 50)
        self.months.setFont(font)

        # Month ComboBox
        self.month_input = QComboBox(self)
        self.month_input.setGeometry(190, 95, 250, 40)
        self.month_input.setFont(QFont("Segoe UI", 12))
        self.month_input.addItems([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        self.month_input.setStyleSheet("background-color: white;")

        # Consumption Label
        self.cons_label = QLabel("Consumption (m³):", self)
        self.cons_label.setGeometry(20, 160, 300, 50)
        self.cons_label.setFont(font)

        # Consumption Input
        self.consumption_input = QLineEdit(self)
        self.consumption_input.setGeometry(330, 160, 100, 50)
        self.consumption_input.setFont(QFont("Segoe UI", 12))
        self.consumption_input.setStyleSheet("background-color: white;")

        # First 10 cubic meter rate
        self.v1l = QLabel("First 10 m³ rate:", self)
        self.v1l.setGeometry(20, 230, 300, 50)
        self.v1l.setFont(font)

        self.v1_input = QLineEdit(self)
        self.v1_input.setGeometry(330, 230, 100, 50)
        self.v1_input.setFont(QFont("Segoe UI", 12))
        self.v1_input.setStyleSheet("background-color: white;")

        # Extra usage rate
        self.v2l = QLabel("Above 10 m³ rate:", self)
        self.v2l.setGeometry(20, 300, 300, 50)
        self.v2l.setFont(font)

        self.v2_input = QLineEdit(self)
        self.v2_input.setGeometry(330, 300, 100, 50)
        self.v2_input.setFont(QFont("Segoe UI", 12))
        self.v2_input.setStyleSheet("background-color: white;")

        # Add Bill Button
        self.add_button = QPushButton("Add Bill", self)
        self.add_button.setGeometry(170, 500, 150, 50)
        self.add_button.setFont(QFont("Segoe UI", 14))
        self.add_button.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.add_button.clicked.connect(self.add_bill)

    def calculate_amount(self, consumption, v1, v2):
        # Calculate the bill based on the two-tier pricing
        if consumption <= 10:
            return consumption * v1
        else:
            return 10 * v1 + (consumption - 10) * v2

    def add_bill(self):
        username = self.users.currentText()
        month = self.month_input.currentText()

        # Validate consumption
        try:
            consumption = float(self.consumption_input.text())
            if consumption < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid positive number for consumption.")
            return

        # Validate first rate
        try:
            v1 = float(self.v1_input.text())
            if v1 < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid positive number for first 10 m³ rate.")
            return

        # Validate extra rate
        try:
            v2 = float(self.v2_input.text())
            if v2 < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid positive number for above 10 m³ rate.")
            return

        # Get user id
        user_id = get_user_id(username)
        if user_id is None:
            QMessageBox.warning(self, "User Not Found", "No user found with that username.")
            return

        # Calculate and save bill
        amount = self.calculate_amount(consumption, v1, v2)
        add_water_bill(user_id, username, month, consumption, amount, v1, v2)
        QMessageBox.information(self, "Success", f"Bill added successfully: {amount:.2f} ₺")
        self.consumption_input.clear()
        self.v1_input.clear()
        self.v2_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPanel()
    window.show()
    sys.exit(app.exec_())
