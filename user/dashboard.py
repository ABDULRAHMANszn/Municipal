from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QTextEdit, QSpinBox,
    QFrame, QPushButton, QVBoxLayout, QMainWindow, QStackedWidget, QCheckBox, QApplication
)
from PyQt5.QtWidgets import QHBoxLayout , QMessageBox
from PyQt5.QtWidgets import QHBoxLayout , QFormLayout
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from user.complainment import Complainment
from suggestion import Suggestion
from user.service import Service
from profile import Profile
from db_manager import create_tables
import sys
from db_manager import *


class WaterSubscriptionForm(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(120, 100, 650, 420)
        self.setStyleSheet("""
            QFrame {
                background-color:#f1f2f6;
                border-radius: 15px;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox, QTextEdit {
                padding: 5px;
                border: 1px solid #aaa;
                border-radius: 5px;
                font-size: 13px;
            }
        """)
        self.setVisible(False)

        self.inputs = {}
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.inputs['address'] = QLineEdit()
        self.inputs['type'] = QComboBox()
        self.inputs['type'].addItems(["Residential", "Commercial", "Governmental", "Industrial", "Agricultural"])
        self.inputs['residents'] = QLineEdit()
        self.inputs['usage'] = QComboBox()
        self.inputs['usage'].setMinimumWidth(200)
        self.inputs['usage'].addItems(["Drinking only", "Home use", "Agricultural", "Industrial", "Swimming Pool"])
        self.inputs['has_tank'] = QComboBox()
        self.inputs['has_tank'].setMinimumWidth(200)
        self.inputs['has_tank'].addItems(["No", "Yes"])
        self.inputs['has_tank'].currentTextChanged.connect(self.toggle_tank_capacity)
        self.inputs['tank_capacity'] = QLineEdit()
        self.inputs['tank_capacity'].setEnabled(False)
        self.inputs['notes'] = QTextEdit()

        form_layout.addRow("Property Address :", self.inputs['address'])
        form_layout.addRow("Property Type :", self.inputs['type'])
        form_layout.addRow("Number of Residents :", self.inputs['residents'])
        form_layout.addRow("Water Usage :", self.inputs['usage'])
        form_layout.addRow("Has Water Tank ?", self.inputs['has_tank'])
        form_layout.addRow("Tank Capacity (L) :", self.inputs['tank_capacity'])
        form_layout.addRow("Notes :", self.inputs['notes'])

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_submit.setStyleSheet("background-color: #196297; color: white; padding: 8px; border-radius: 5px;")
        self.btn_cancel.setStyleSheet("background-color: #ccc; padding: 8px; border-radius: 5px;")
        self.btn_submit.clicked.connect(self.submit_form)
        self.btn_cancel.clicked.connect(self.hide)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def toggle_tank_capacity(self, text):
        self.inputs['tank_capacity'].setEnabled(text == "Yes")

    def submit_form(self):
        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QTextEdit):
                value = widget.toPlainText().strip()
            elif isinstance(widget, QLineEdit):
                value = widget.text().strip()
            elif isinstance(widget, QComboBox):
                value = widget.currentText().strip()
            else:
                value = ""
            data[key] = value

        missing = []
        for key, value in data.items():
            if key == 'tank_capacity' and data.get('has_tank') == "No":
                continue  # تجاهل التحقق إذا ما عنده خزان
            if not value:
                missing.append(key)

        if missing:
            msg = "Please fill in all required fields"
            QMessageBox.warning(self, "Missing Data", msg)
            return

        try:
            save_water_subscription(data)
            QMessageBox.information(self, "Success", "Subscription saved successfully.")
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{str(e)}")




class ElectricitySubscriptionForm(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(120, 100, 650, 400)
        self.setStyleSheet("""
            QFrame { background-color:#f1f2f6; border-radius: 15px; }
            QLabel { font-size: 14px; }
            QLineEdit, QComboBox, QTextEdit {
                padding: 5px; border: 1px solid #aaa; border-radius: 5px; font-size: 13px;
            }
        """)
        self.setVisible(False)

        self.inputs = {}
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.inputs['address'] = QLineEdit()
        self.inputs['type'] = QComboBox()
        self.inputs['type'].setMinimumWidth(200)
        self.inputs['type'].addItems(["Residential", "Commercial", "Industrial", "Governmental"])
        self.inputs['phase'] = QComboBox()
        self.inputs['phase'].setMinimumWidth(200)
        self.inputs['phase'].addItems(["Single Phase", "Three Phase"])
        self.inputs['usage'] = QLineEdit()
        self.inputs['generator'] = QComboBox()
        self.inputs['generator'].setMinimumWidth(200)
        self.inputs['generator'].addItems(["No", "Yes"])
        self.inputs['notes'] = QTextEdit()

        form_layout.addRow("Property Address:", self.inputs['address'])
        form_layout.addRow("Property Type:", self.inputs['type'])
        form_layout.addRow("Electricity Phase:", self.inputs['phase'])
        form_layout.addRow("Estimated Usage (kWh):", self.inputs['usage'])
        form_layout.addRow("Need Generator?", self.inputs['generator'])
        form_layout.addRow("Notes:", self.inputs['notes'])

        layout.addLayout(form_layout)
        btn_layout = QHBoxLayout()
        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_submit.setStyleSheet("background-color: #196297; color: white; padding: 8px; border-radius: 5px;")
        self.btn_cancel.setStyleSheet("background-color: #ccc; padding: 8px; border-radius: 5px;")
        self.btn_submit.clicked.connect(self.submit_form)
        self.btn_cancel.clicked.connect(self.hide)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def submit_form(self):
        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QTextEdit):
                value = widget.toPlainText().strip()
            elif isinstance(widget, QLineEdit):
                value = widget.text().strip()
            elif isinstance(widget, QComboBox):
                value = widget.currentText().strip()
            else:
                value = ""
            data[key] = value

        missing = [key for key in data if not data[key]]

        if missing:
            QMessageBox.warning(self, "Missing Data", "Please fill in all required fields.")
            return

        try:
            print("Electricity Subscription Saved:")
            print(data)
            QMessageBox.information(self, "Success", "Electricity subscription submitted successfully.")
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{str(e)}")

class CleaningSubscriptionForm(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(120, 100, 650, 350)
        self.setStyleSheet("""
            QFrame { background-color:#f1f2f6; border-radius: 15px; }
            QLabel { font-size: 14px; }
            QLineEdit, QTextEdit, QComboBox {
                padding: 5px; border: 1px solid #aaa; border-radius: 5px; font-size: 13px;
            }
        """)
        self.setVisible(False)

        self.inputs = {}
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.inputs['address'] = QLineEdit()
        self.inputs['property_type'] = QComboBox()
        self.inputs['property_type'].setMinimumWidth(200)
        self.inputs['property_type'].addItems(["House", "Building", "Institution", "Other"])
        self.inputs['frequency'] = QComboBox()
        self.inputs['frequency'].setMinimumWidth(200)
        self.inputs['frequency'].addItems(["Daily", "Weekly", "Monthly"])
        self.inputs['notes'] = QTextEdit()

        form_layout.addRow("Address:", self.inputs['address'])
        form_layout.addRow("Property Type:", self.inputs['property_type'])
        form_layout.addRow("Cleaning Frequency:", self.inputs['frequency'])
        form_layout.addRow("Notes:", self.inputs['notes'])

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_submit.setStyleSheet("background-color: #196297; color: white; padding: 8px; border-radius: 5px;")
        self.btn_cancel.setStyleSheet("background-color: #ccc; padding: 8px; border-radius: 5px;")
        self.btn_submit.clicked.connect(self.submit_form)
        self.btn_cancel.clicked.connect(self.hide)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def submit_form(self):
        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QTextEdit):
                value = widget.toPlainText().strip()
            elif isinstance(widget, QLineEdit):
                value = widget.text().strip()
            elif isinstance(widget, QComboBox):
                value = widget.currentText().strip()
            else:
                value = ""
            data[key] = value

        missing = [key for key in data if not data[key]]
        if missing:
            QMessageBox.warning(self, "Missing Data", "Please fill in all required fields.")
            return

        try:
            print("Cleaning Subscription Saved:")
            print(data)
            QMessageBox.information(self, "Success", "Cleaning subscription submitted successfully.")
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\\n{str(e)}")

class GasSubscriptionForm(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(120, 100, 650, 400)
        self.setStyleSheet("""
            QFrame {
                background-color:#f1f2f6;
                border-radius: 15px;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox, QTextEdit {
                padding: 5px;
                border: 1px solid #aaa;
                border-radius: 5px;
                font-size: 13px;
            }
        """)
        self.setVisible(False)

        self.inputs = {}
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.inputs['address'] = QLineEdit()
        self.inputs['property_type'] = QComboBox()
        self.inputs['property_type'].setMinimumWidth(200)
        self.inputs['property_type'].addItems(["Residential", "Commercial", "Industrial"])
        self.inputs['stove_type'] = QComboBox()
        self.inputs['stove_type'].setMinimumWidth(200)
        self.inputs['stove_type'].addItems(["1-burner", "2-burner", "Built-in"])
        self.inputs['cylinder_size'] = QComboBox()
        self.inputs['cylinder_size'].setMinimumWidth(200)
        self.inputs['cylinder_size'].addItems(["Small", "Medium", "Large"])
        self.inputs['usage'] = QLineEdit()
        self.inputs['notes'] = QTextEdit()

        form_layout.addRow("Property Address:", self.inputs['address'])
        form_layout.addRow("Property Type:", self.inputs['property_type'])
        form_layout.addRow("Stove Type:", self.inputs['stove_type'])
        form_layout.addRow("Cylinder Size:", self.inputs['cylinder_size'])
        form_layout.addRow("Usage:", self.inputs['usage'])
        form_layout.addRow("Notes:", self.inputs['notes'])

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_submit.setStyleSheet("background-color: #196297; color: white; padding: 8px; border-radius: 5px;")
        self.btn_cancel.setStyleSheet("background-color: #ccc; padding: 8px; border-radius: 5px;")
        self.btn_submit.clicked.connect(self.submit_form)
        self.btn_cancel.clicked.connect(self.hide)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def submit_form(self):
        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QTextEdit):
                value = widget.toPlainText().strip()
            elif isinstance(widget, QLineEdit):
                value = widget.text().strip()
            elif isinstance(widget, QComboBox):
                value = widget.currentText().strip()
            else:
                value = ""
            data[key] = value

        missing = [key for key in data if key != 'notes' and not data[key]]
        if missing:
            msg = "Please fill in all required fields."
            QMessageBox.warning(self, "Missing Data", msg)
            return

        try:
            save_gas_subscription(data)
            QMessageBox.information(self, "Success", "Gas subscription submitted successfully.")
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{str(e)}")


class VisaDigitalForm(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(120, 100, 650, 400)
        self.setStyleSheet("""
            QFrame {
                background-color:#f1f2f6;
                border-radius: 15px;
            }
            QLabel {
                font-size: 13px;
            }
            QLineEdit {
                padding: 4px;
                border: 1px solid #aaa;
                border-radius: 4px;
                font-size: 13px;
            }
        """)
        self.setVisible(False)

        self.inputs = {}
        layout = QVBoxLayout()

        title = QLabel("Payment Information")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: black;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()
        self.inputs['card_number'] = QLineEdit()
        self.inputs['balance'] = QLineEdit("₺0,00")
        self.inputs['balance'].setReadOnly(True)
        self.inputs['topup'] = QLineEdit()
        form_layout.addRow("Transportation Card Number:", self.inputs['card_number'])
        form_layout.addRow("Current Balance:", self.inputs['balance'])
        form_layout.addRow("Balance to be loaded:", self.inputs['topup'])

        credit_title = QLabel("Credit/Debit Card Information")
        credit_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        credit_title.setStyleSheet("color: black;")
        credit_title.setAlignment(Qt.AlignCenter)

        credit_form = QFormLayout()
        self.inputs['owner'] = QLineEdit()
        self.inputs['credit_card'] = QLineEdit()
        credit_form.addRow("Cardholder Name Surname:", self.inputs['owner'])
        credit_form.addRow("Card No:", self.inputs['credit_card'])

        date_row = QHBoxLayout()
        self.inputs['month'] = QLineEdit()
        self.inputs['year'] = QLineEdit()
        self.inputs['cvv'] = QLineEdit()
        self.inputs['month'].setPlaceholderText("month")
        self.inputs['year'].setPlaceholderText("year")
        self.inputs['cvv'].setPlaceholderText("CVV code")
        date_row.addWidget(self.inputs['month'])
        date_row.addWidget(self.inputs['year'])
        date_row.addWidget(self.inputs['cvv'])

        self.checkbox = QCheckBox("I have read and accept the distance sales contract.")

        btn_layout = QHBoxLayout()
        submit_btn = QPushButton("Pay Now")
        submit_btn.setStyleSheet("background-color: #196297; color: white; padding: 6px; border-radius: 5px;")
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("padding: 6px;")
        submit_btn.clicked.connect(self.submit_form)
        cancel_btn.clicked.connect(self.hide)
        btn_layout.addStretch()
        btn_layout.addWidget(submit_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(form_layout)
        layout.addWidget(credit_title)
        layout.addLayout(credit_form)
        layout.addLayout(date_row)
        layout.addWidget(self.checkbox)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def submit_form(self):
        data = {}
        for key, field in self.inputs.items():
            data[key] = field.text().strip()

        if not all(data.values()) or not self.checkbox.isChecked():
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields and accept the agreement.")
            return

        try:
            save_visa_subscription(data)
            QMessageBox.information(self, "Successful", "Payment completed successfully.")
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error:\n{str(e)}")




class Main(QWidget):
    def __init__(self, parent_frame):
        super().__init__(parent_frame)

        self.subl = QLabel("Subscriptions", self)
        self.subl.setFont(QFont("Segoe UI", 25, QFont.Bold))
        self.subl.setAlignment(Qt.AlignCenter)
        self.subl.setGeometry(320, 45, 300, 60)
        self.subl.setStyleSheet("color: #1E2A38;")

        self.water_form = WaterSubscriptionForm(self)
        self.electricity_form = ElectricitySubscriptionForm(self)
        self.cleaning_form = CleaningSubscriptionForm(self)
        self.gas_form = GasSubscriptionForm(self)
        self.visa_form = VisaDigitalForm(self)

        self.create_fun_card(90, 130, "../images/Su.jpeg", "Water Subscription", "Subscribe", self.show_water_form)
        self.create_fun_card(340, 130, "../images/elec.jpg", "Electricity Subscription", "Subscribe", self.show_electricity_form)
        self.create_fun_card(590, 130, "../images/clean.jpg", "Cleaning Subscription", "Subscribe",self.show_cleaning_form)
        self.create_fun_card(90, 420, "../images/gas.jpg", "Gas Subscription", "Subscribe", self.show_gas_form)
        self.create_fun_card(340, 420, "../images/visa.jpg", "Visa Digital", "Subscribe", self.show_visa_form)
        self.create_fun_card(590, 420, "../images/statf.jpeg", "Staff", "View")

    def create_fun_card(self, x, y, image_path, title_text, button_text, button_action=None):
        card = QFrame(self)
        card.setGeometry(x, y, 220, 270)
        card.setStyleSheet("""
            QFrame {
                background-color: #fefefe;
                border-radius: 15px;
                border: 1px solid #ddd;
            }
        """)

        img = QLabel(card)
        img.setGeometry(10, 10, 200, 120)
        pixmap = QPixmap(image_path).scaled(200, 120, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        img.setPixmap(pixmap)
        img.setAlignment(Qt.AlignCenter)
        img.setStyleSheet("border-radius: 10px;")

        title = QLabel(title_text, card)
        title.setGeometry(10, 140, 200, 30)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title.setStyleSheet("color: #333;")

        button = QPushButton(button_text, card)
        button.setGeometry(45, 200, 130, 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #ff5252;
                color: white;
                font-size: 20px;
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #ff1744;
            }
        """)
        if button_action:
            button.clicked.connect(button_action)

    def show_water_form(self):
        self.water_form.raise_()
        self.water_form.setVisible(True)

    def show_electricity_form(self):
        self.electricity_form.raise_()
        self.electricity_form.setVisible(True)

    def show_cleaning_form(self):
         self.cleaning_form.raise_()
         self.cleaning_form.setVisible(True)

    def show_gas_form(self):
        self.gas_form.raise_()
        self.gas_form.setVisible(True)

    def show_visa_form(self):
        self.visa_form.raise_()
        self.visa_form.setVisible(True)


class Dashboard(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setFixedSize(1244, 700)
        self.setWindowTitle("Dashboard")
        self.setWindowIcon(QIcon("../images/icon.png"))

        self.c = QFrame(self)
        self.setCentralWidget(self.c)
        self.setup_form()


    def setup_form(self):
        self.right_frame = QFrame(self.c)
        self.right_frame.setGeometry(350, 0, 894, 700)
        self.right_frame.setStyleSheet("background-color: #f1f2f6;")

        self.left_frame = QFrame(self.c)
        self.left_frame.setGeometry(0, 0, 350, 700)
        self.left_frame.setStyleSheet("background-color: #1E2A38;")

        self.label = QLabel(self.left_frame)
        pixmap = QPixmap("../images/icon2-Photoroom.png").scaled(220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)
        self.label.setGeometry(60, 5, pixmap.width(), pixmap.height())

        welcomL = QLabel(f"Hello {self.username}", self.left_frame)
        welcomL.setFont(QFont("Segoe UI", 18, QFont.Bold))
        welcomL.setAlignment(Qt.AlignCenter)
        welcomL.setGeometry(5, 190, 350, 60)
        welcomL.setStyleSheet("color: white;")

        button_style = """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 25px;
                text-align: left;
                padding-left: 60px;
            }
            QPushButton:checked {
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }
        """

        self.btn_main = QPushButton(" Main", self.left_frame)
        self.btn_main.setGeometry(0, 250, 350, 50)
        self.btn_main.setCheckable(True)
        self.btn_main.setStyleSheet(button_style)
        self.btn_main.setIcon(QIcon("../images/home.png"))
        self.btn_main.setIconSize(QSize(20, 20))

        self.btn_Subsc = QPushButton(" My Subscriptions", self.left_frame)
        self.btn_Subsc.setGeometry(0, 300, 350, 50)
        self.btn_Subsc.setCheckable(True)
        self.btn_Subsc.setStyleSheet(button_style)
        self.btn_Subsc.setIcon(QIcon("../images/m.png"))
        self.btn_Subsc.setIconSize(QSize(22, 22))

        self.btn_service = QPushButton(" Service Request", self.left_frame)
        self.btn_service.setGeometry(0, 350, 350, 50)
        self.btn_service.setCheckable(True)
        self.btn_service.setStyleSheet(button_style)
        self.btn_service.setIcon(QIcon("../images/ser.png"))
        self.btn_service.setIconSize(QSize(22, 22))

        self.btn_complaint = QPushButton(" Complaint", self.left_frame)
        self.btn_complaint.setGeometry(0, 400, 350, 50)
        self.btn_complaint.setCheckable(True)
        self.btn_complaint.setStyleSheet(button_style)
        self.btn_complaint.setIcon(QIcon("../images/con.png"))
        self.btn_complaint.setIconSize(QSize(22, 22))

        self.btn_suggestion = QPushButton(" Suggestion", self.left_frame)
        self.btn_suggestion.setGeometry(0, 450, 350, 50)
        self.btn_suggestion.setCheckable(True)
        self.btn_suggestion.setStyleSheet(button_style)
        self.btn_suggestion.setIcon(QIcon("../images/suggestion.png"))
        self.btn_suggestion.setIconSize(QSize(22, 22))

        self.btn_profile = QPushButton(" Profile", self.left_frame)
        self.btn_profile.setGeometry(0, 500, 350, 50)
        self.btn_profile.setCheckable(True)
        self.btn_profile.setStyleSheet(button_style)
        self.btn_profile.setIcon(QIcon("../images/pro.png"))
        self.btn_profile.setIconSize(QSize(22, 22))

        self.btn_signout = QPushButton(" Sign out", self.left_frame)
        self.btn_signout.setGeometry(0, 600, 350, 50)
        self.btn_signout.setCheckable(True)
        self.btn_signout.setStyleSheet(button_style)
        self.btn_signout.setIcon(QIcon("../images/out.png"))
        self.btn_signout.setIconSize(QSize(22, 22))

        self.stack = QStackedWidget(self.right_frame)
        self.stack.setGeometry(0, 0, 894, 700)

        self.page_main = Main(self.stack)
        self.page_subs = Main(self.stack)
        self.page_service = Service(self.username)
        self.page_complaint = Complainment(self.username)
        self.page_suggestion = Suggestion(self.username)
        self.page_profile = Profile(self.username)

        self.stack.addWidget(self.page_main)
        self.stack.addWidget(self.page_subs)
        self.stack.addWidget(self.page_service)
        self.stack.addWidget(self.page_complaint)
        self.stack.addWidget(self.page_suggestion)
        self.stack.addWidget(self.page_profile)

        self.setup_button()

    def setup_button(self):
        self.btn_main.clicked.connect(lambda: self.switch_page(0, self.btn_main))
        self.btn_Subsc.clicked.connect(lambda: self.switch_page(1, self.btn_Subsc))
        self.btn_service.clicked.connect(lambda: self.switch_page(2, self.btn_service))
        self.btn_complaint.clicked.connect(lambda: self.switch_page(3, self.btn_complaint))
        self.btn_suggestion.clicked.connect(lambda: self.switch_page(4, self.btn_suggestion))
        self.btn_profile.clicked.connect(lambda: self.switch_page(5, self.btn_profile))

        self.switch_page(0, self.btn_main)

    def switch_page(self, index, active_button):
        self.stack.setCurrentIndex(index)
        for btn in [
            self.btn_main, self.btn_Subsc, self.btn_service,
            self.btn_complaint, self.btn_suggestion, self.btn_profile,
        ]:
            btn.setChecked(btn == active_button)


if __name__ == "__main__":
    create_tables()
    create_water_subscription_table()
    create_electricity_subscription_table()
    create_cleaning_subscription_table()
    create_gas_subscription_table()
    app = QApplication(sys.argv)
    window = Dashboard("abood")
    window.show()
    sys.exit(app.exec_())
