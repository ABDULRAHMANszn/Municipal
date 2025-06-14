import sys

from all_Requests import Requests
from all_users import ManageUsers
from service import Service
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFrame, QLabel, QDesktopWidget,
    QPushButton, QStackedWidget
)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt


class Employee_Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dashboard")
        self.setWindowIcon(QIcon("images/icon.png"))
        self.move(0,0)
        self.setFixedSize(1400, 700)

        self.central = QFrame(self)
        self.setCentralWidget(self.central)

        self.left_frame = QFrame(self.central)
        self.left_frame.setGeometry(0, 0, 300, 700)
        self.left_frame.setStyleSheet("background-color: #196297;")

        self.right_frame = QStackedWidget(self.central)
        self.right_frame.setGeometry(300, 0, 1100, 700)

        self.setup_left_panel()
        self.setup_right_views()

    def setup_left_panel(self):
        font = QFont("Arial", 18)
        welcomL = QLabel("Dashboard Employee", self.left_frame)
        welcomL.setFont(font)
        welcomL.setAlignment(Qt.AlignCenter)
        welcomL.setGeometry(0, 0, 244, 100)
        welcomL.setStyleSheet("color: white;")

        logo = QLabel(self.left_frame)
        pixmap = QPixmap("images/icon2-Photoroom.png").scaled(200, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setGeometry(40, 70, pixmap.width(), pixmap.height())

        # Buttons
        self.servicel = QPushButton("Users", self.left_frame)
        self.Complaintl = QPushButton("Payments", self.left_frame)
        self.Suggestionl = QPushButton("Requests", self.left_frame)

        self.Options_labels = [self.servicel, self.Complaintl, self.Suggestionl]

        for i, btn in enumerate(self.Options_labels):
            btn.setGeometry(0, 400 + i * 50, 300, 50)
            btn.setStyleSheet("""
                color: white;
                border-bottom: 1px solid white;
                font: 20px Arial, sans-serif;
            """)

        self.servicel.clicked.connect(lambda: self.right_frame.setCurrentIndex(0))
        self.Complaintl.clicked.connect(lambda: self.right_frame.setCurrentIndex(1))
        self.Suggestionl.clicked.connect(lambda: self.right_frame.setCurrentIndex(2))

    def setup_right_views(self):
        self.service_widget = ManageUsers()  # Frame 0

        # Dummy placeholders for others
        self.suggestions_widget = Requests()

        self.receipts_widget = QLabel("Receipts Page")
        self.receipts_widget.setAlignment(Qt.AlignCenter)

        # Add to stacked widget
        self.right_frame.addWidget(self.service_widget)
        self.right_frame.addWidget(self.complaints_widget)
        self.right_frame.addWidget(self.suggestions_widget)
        self.right_frame.addWidget(self.receipts_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Employee_Dashboard()
    window.show()
    sys.exit(app.exec_())
