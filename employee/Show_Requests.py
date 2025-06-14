from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QPushButton
import sqlite3

class ViewRequestsWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("User Requests Overview")
        self.setGeometry(50, 50, 1100, 600)

        self.table = QTableWidget(self)
        self.table.setGeometry(50, 40, 1000, 500)
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["User Id", "Username", "Name", "Surname", "Type", "Description", "More Info","Status", "Edit", "Delete"])

        self.load_requests(user_id)
        print(user_id)
    def load_requests(self, user_id):

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, name, surname FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return

        user_id, username, name, surname = user
        all_rows = []

        # Load services
        cursor.execute("SELECT description, address FROM requests WHERE user_id = ?", (user_id,))
        for desc, address in cursor.fetchall():
            all_rows.append(["Service", desc, address])

        # Load complaints
        cursor.execute("SELECT title, description FROM complaints WHERE user_id = ?", (user_id,))
        for title, desc in cursor.fetchall():
            all_rows.append(["Complaint", title, desc])

        # Load suggestions
        cursor.execute("SELECT suggestion, proposed_solution FROM suggestions WHERE user_id = ?", (user_id,))
        for suggestion, solution in cursor.fetchall():
            all_rows.append(["Suggestion", suggestion, solution])

        self.table.setRowCount(len(all_rows))
        for row_index, row_data in enumerate(all_rows):
            self.table.setItem(row_index, 0, QTableWidgetItem(str(user_id)))
            self.table.setItem(row_index, 1, QTableWidgetItem(username))
            self.table.setItem(row_index, 2, QTableWidgetItem(name))
            self.table.setItem(row_index, 3, QTableWidgetItem(surname))
            self.table.setItem(row_index, 4, QTableWidgetItem(row_data[0]))  # Type
            self.table.setItem(row_index, 5, QTableWidgetItem(row_data[1]))  # Description
            self.table.setItem(row_index, 6, QTableWidgetItem(row_data[2]))  # More Info
            self.table.setItem(row_index, 7, QTableWidgetItem(self.get_request_status_by_id(user_id)))
            print(self.get_request_status_by_id(user_id))
            self.table.setItem(row_index, 9, QTableWidgetItem("Delete"))     # Placeholder
            view_button = QPushButton("Edit_status")
            view_button.setStyleSheet("background-color: blue;")
            view_button.setStyleSheet("background-color: #196297; padding: 8px; color: white;")
            # view_button.clicked.connect(lambda _, uid=user_id: self.edit_button(uid))
            view_button.clicked.connect(self.edit_button(user_id))
            self.table.setCellWidget(row_index, 8, view_button)

        conn.close()

    def get_request_status_by_id(self, request_id):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT status FROM requests WHERE id = ?", (request_id,))
        result = c.fetchone()
        conn.close()

        if result:
            return result[0]  # Return the status value
        else:
            return None  # ID not found

    def edit_button(self, user_id):
        return lambda: self.edit_button_clicked(user_id)
    def edit_button_clicked(self, userr_id):
        button = self.sender()  # Get the clicked button
        index = self.table.indexAt(button.pos())  # Get the index of the button in the table
        row = index.row()  # Get the row number

        desc = self.table.item(row, 5).text()
        type_value = self.table.item(row, 4).text()
        if type_value == "Service":
            type_value = "requests"
        elif type_value == "Complaint":
            type_value = "complaints"
        else:
            type_value = "suggestions"

        self.update_status_to_finished_for_segguestion(type_value, userr_id)

        # if type_value == "Complaint" or type_value == "Service":
        #     self.update_status_to_finished(type_value, userr_id, desc)
        # else:
        #     self.update_status_to_finished_for_segguestion(type_value, userr_id)

    def update_status_to_finished(table_name, request_id, description):
        if table_name not in ['requests', 'complaints', 'suggestions']:
            print("Error: Invalid table name.")
            return

        try:
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            c.execute(f"""
                UPDATE {table_name}
                SET status = 'finished'
                WHERE id = ? AND description = ?
            """, (request_id, description))

            conn.commit()
            print(f"Status updated to 'finished' in {table_name} for ID {request_id} and description.")

        except sqlite3.Error as e:
            print("Database error:", e)

        finally:
            conn.close()


def update_status_to_finished_for_segguestion(table_name, request_id):

    if table_name not in ['requests', 'complaints', 'suggestions']:
        print("Error: Invalid table name.")
        return

    try:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        c.execute(f"""
            UPDATE {table_name}
            SET status = 'finished'
            WHERE id = ?
        """, (request_id,))

        conn.commit()
        print(f"Status updated to 'finished' in {table_name} for ID {request_id}.")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        conn.close()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = ViewRequestsWindow(34234)
    window.show()
    sys.exit(app.exec_())
