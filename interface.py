from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QStackedWidget, QHBoxLayout,QCalendarWidget
)
from PyQt5.QtCore import Qt, QDate
import pymysql
import sys
import hashlib

connection = pymysql.connect(
    host='localhost',
    user='rysch01',
    password='SQLP4ssword1!',
    database='cafeteria',
)
cursor = connection.cursor()

class LoginPage(QWidget):
    global cursor
    def __init__(self, switch_to_admin, switch_to_student):
        super().__init__()
        self.switch_to_admin = switch_to_admin
        self.switch_to_student = switch_to_student
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel('Login Page', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title_label)

        self.pid_input = QLineEdit(self)
        self.pid_input.setPlaceholderText('Enter PID')
        layout.addWidget(self.pid_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.error_display = QTextEdit(self)
        self.error_display.setReadOnly(True)
        self.error_display.setStyleSheet('color: red;')
        layout.addWidget(self.error_display)

        self.setLayout(layout)

    def handle_login(self):
        pid = self.pid_input.text()
        password = self.password_input.text()
        self.error_display.clear()

        try:
            cursor.execute("SELECT role, password_hash FROM Students WHERE pid = %s", (pid,))
            result = cursor.fetchone()

            if result:
                role, password_hash = result
                if password_hash == password:  # Simplified for now; replace with hashed check
                    if role == 'admin':
                        self.switch_to_admin()
                    else:
                        self.switch_to_student(pid)
                else:
                    self.error_display.setText("Error: Incorrect password.")
            else:
                self.error_display.setText("Error: PID not found.")
        except Exception as e:
            self.error_display.setText(f"Error: {e}")
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_login(self):
        pid = self.pid_input.text()
        password = self.password_input.text()
        self.error_display.clear()

        try:

            cursor.execute("SELECT role, password_hash FROM Students WHERE pid = %s", (pid,))
            result = cursor.fetchone()

            if result:
                role, password_hash = result
                if password_hash == self.hash_password(password):  # Secure hashed comparison
                    if role == 'admin':
                        self.switch_to_admin()
                    else:
                        self.switch_to_student(pid)
                else:
                    self.error_display.setText("Error: Incorrect password.")
            else:
                self.error_display.setText("Error: PID not found.")
        except Exception as e:
            self.error_display.setText(f"Error: {e}")


class AdminView(QWidget):
    global cursor
    def __init__(self, switch_to_login, backend):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.backend = backend
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel('Admin Dashboard', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title_label)

        # Buttons for admin functionalities
        manage_students_button = QPushButton("Manage Students")
        manage_students_button.clicked.connect(self.show_manage_students)
        layout.addWidget(manage_students_button)

        manage_menu_button = QPushButton("Manage Menu")
        manage_menu_button.clicked.connect(self.show_manage_menu)
        layout.addWidget(manage_menu_button)

        view_transactions_button = QPushButton("View Transactions")
        view_transactions_button.clicked.connect(self.show_view_transactions)
        layout.addWidget(view_transactions_button)

        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.switch_to_login)
        layout.addWidget(logout_button)

        self.setLayout(layout)

    def show_manage_students(self):
        self.clear_screen()
        layout = QVBoxLayout()

        title = QLabel("Manage Students")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # Example: Display student details in a table
        student_table = QTableWidget()
        student_data = self.backend.get_all_students()
        student_table.setRowCount(len(student_data))
        student_table.setColumnCount(4)
        student_table.setHorizontalHeaderLabels(["PID", "Name", "Balance", "To-Go Boxes"])

        for row, student in enumerate(student_data):
            for col, value in enumerate(student):
                student_table.setItem(row, col, QTableWidgetItem(str(value)))

        layout.addWidget(student_table)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.initUI)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def show_manage_menu(self):
        self.clear_screen()
        layout = QVBoxLayout()

        title = QLabel("Manage Menu")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # Example: Display menu items in a table
        menu_table = QTableWidget()
        menu_data = self.backend.get_all_menu_items()
        menu_table.setRowCount(len(menu_data))
        menu_table.setColumnCount(5)
        menu_table.setHorizontalHeaderLabels(["Item ID", "Name", "Quantity", "Price", "Meal Type"])

        for row, item in enumerate(menu_data):
            for col, value in enumerate(item):
                menu_table.setItem(row, col, QTableWidgetItem(str(value)))

        layout.addWidget(menu_table)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.initUI)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def show_view_transactions(self):
        self.clear_screen()
        layout = QVBoxLayout()

        title = QLabel("View Transactions")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # Example: Display transactions in a table
        transaction_table = QTableWidget()
        transaction_data = self.backend.get_all_transactions()
        transaction_table.setRowCount(len(transaction_data))
        transaction_table.setColumnCount(5)
        transaction_table.setHorizontalHeaderLabels(
            ["Transaction ID", "Student ID", "Item ID", "Type", "Amount"]
        )

        for row, transaction in enumerate(transaction_data):
            for col, value in enumerate(transaction):
                transaction_table.setItem(row, col, QTableWidgetItem(str(value)))

        layout.addWidget(transaction_table)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.initUI)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def clear_screen(self):
        # Clear the current screen to show new content
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()


class StudentView(QWidget):
    global cursor

    def __init__(self, pid, switch_to_login, backend):
        super().__init__()
        self.pid = pid
        self.switch_to_login = switch_to_login
        self.backend = backend
        self.selected_date = QDate.currentDate()
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel('Student View', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title_label)

        # Display student details

        
        current_user=self.backend.get_user_info(self.pid)
        # print(current_user)
        current_user={
            'pid': current_user[0],
            'first': current_user[1],
            'last': current_user[2],
            'balance': current_user[3],
            'to_go_remaining': current_user[4],
            'role': current_user[6],
        }
        # print(f'Account Balance: ${current_user["balance"]}')
        # print(f'To-Go Boxes Remaining: {current_user["to_go_remaining"]}/2')

        # print("Your Transaction History")
        cursor.execute('SELECT * FROM Transactions T WHERE T.pid=%s', current_user["pid"])
        result = cursor.fetchall()
        print(result)
    


        student_name = f'{current_user["first"]} {current_user["last"]}'
        pid = current_user['pid']

        account_balance = current_user['balance']
        togo_boxes = current_user['to_go_remaining']

        layout.addWidget(QLabel(f"Name: {student_name}"))
        layout.addWidget(QLabel(f"PID: {pid}"))
        layout.addWidget(QLabel(f"Account Balance: ${account_balance:.2f}"))
        layout.addWidget(QLabel(f"To-Go Boxes Available: {togo_boxes}"))


        self.date_label = QLabel(f"Menu for {self.selected_date.toString('yyyy-MM-dd')}", self)
        layout.addWidget(self.date_label)

        # Add calendar widget with today's date selected
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(self.selected_date)  # Set today's date
        self.calendar.clicked.connect(self.select_date)
        layout.addWidget(self.calendar)

        # Label to display the currently selected date

        self.menu=QTableWidget(self)
        self.menu.setColumnCount(4)
        self.menu.setHorizontalHeaderLabels(['Meal', 'Item', 'Price', 'Calories'])
        layout.addWidget(self.menu)

        # Today's menu based on selected_date
        self.update_menu_based_on_date(self.selected_date)

    
        self.payment_history_label = QLabel(f"Payment History", self)
        layout.addWidget(self.payment_history_label)

        self.payment_history=QTableWidget(self)
        self.payment_history.setColumnCount(5)
        self.payment_history.setHorizontalHeaderLabels(['Date', 'Meal', 'Item', 'Price', 'Type'])
        cursor.execute('SELECT * FROM Transactions T LEFT JOIN Menu M ON M.item_id = T.item_id WHERE T.pid = %s', pid)
        result=cursor.fetchall()
        print(result[0])
        print('here', result[0][4], result[0][7], result[0][6],  result[0][10], result[0][3])
        # 4 (date)
        # 7 (meal)
        # 6 (item)
        # 10 (price)
        # 3 (type)
 


        self.payment_history.setRowCount(len(result))
        # # go through the each row and column data
        for ri, rdata in enumerate(result):
            self.payment_history.setItem(ri, 0, QTableWidgetItem(str(rdata[4])))
            self.payment_history.setItem(ri, 1, QTableWidgetItem(str(rdata[8])))
            self.payment_history.setItem(ri, 2, QTableWidgetItem(str(rdata[6])))
            self.payment_history.setItem(ri, 3, QTableWidgetItem(str(rdata[10])))
            self.payment_history.setItem(ri, 4, QTableWidgetItem(str(rdata[3])))


        layout.addWidget(self.payment_history)


        # Logout button
        self.logout_button = QPushButton('Logout', self)
        self.logout_button.clicked.connect(self.switch_to_login)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def select_date(self, date):
        """
        Update the selected date when the user clicks on a date in the calendar.
        """
        self.selected_date = date
        self.date_label.setText(f"Selected Date: {self.selected_date.toString('yyyy-MM-dd')}")
        self.update_menu_based_on_date(self.selected_date)

    def update_menu_based_on_date(self, date):
        """
        Query and print today's menu based on the selected date.
        """
        # Clear rows
        self.menu.setRowCount(0)
        cursor.execute('SELECT * FROM Menu M WHERE available_date=%s', date.toString('yyyy-MM-dd'))
        result = cursor.fetchall()


        meal = {'breakfast': 0, 'lunch': 1, 'dinner': 2}
        result = sorted(result, key=lambda x: meal.get(x[3], 3))  # Default to 3 for unknown types


        self.menu.setRowCount(len(result))
        # go through the each row and column data
        for ri, rdata in enumerate(result):
            self.menu.setItem(ri, 0, QTableWidgetItem(str(rdata[3])))
            self.menu.setItem(ri, 1, QTableWidgetItem(str(rdata[1])))
            self.menu.setItem(ri, 2, QTableWidgetItem(str(rdata[5])))
            self.menu.setItem(ri, 3, QTableWidgetItem(str(rdata[2])))



    def show_manage_students_screen(self):
        self.clear_screen()
        layout = QVBoxLayout()

        title = QLabel("Manage Students")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # Add table or form to edit student details
        # Example: Show list of students in a table and allow admin to edit or delete records
        # (Use QTableView or a similar widget)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_admin_screen)
        layout.addWidget(back_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)



class MainWindow(QWidget):
    global cursor

    def __init__(self):
        super().__init__()
        self.backend = DatabaseBackend()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cafeteria Database Interface')
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()

        self.login_page = LoginPage(self.show_admin_view, self.show_student_view)
        self.admin_view = AdminView(self.show_login_page, self.backend)
        self.student_view = None  # Initialized dynamically

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.admin_view)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.show_login_page()

    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_admin_view(self):
        self.admin_view = AdminView(self.show_login_page, self.backend)
        self.stacked_widget.addWidget(self.admin_view)
        self.stacked_widget.setCurrentWidget(self.admin_view)
    
    def show_student_view(self, pid):
        self.student_view = StudentView(pid, self.show_login_page, self.backend)
        self.stacked_widget.addWidget(self.student_view)
        self.stacked_widget.setCurrentWidget(self.student_view)


class DatabaseBackend:
    global cursor

    def get_user_info(self, pid):
        query = "SELECT * FROM Students WHERE pid = %s"
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        return result if result else 0
    
    def get_student_name(self, pid):
        query = "SELECT first_name, last_name FROM Students WHERE pid = %s"
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        return f"{result[0]} {result[1]}" if result else "Unknown"

    def get_account_balance(self, pid):
        query = "SELECT meal_balance FROM Students WHERE pid = %s"
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        return result[0] if result else 0.0

    def get_togo_boxes(self, pid):
        query = "SELECT to_go_boxes_remaining FROM Students WHERE pid = %s"
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        return result[0] if result else 0
    
    def get_menu_for_date(self, date, meal_type):
        query = """
        SELECT * FROM Menu WHERE available_date = %s AND meal_type = %s AND quantity > 0
        """
        cursor.execute(query, (date, meal_type))
        return cursor.fetchall()

    def process_transaction(self, pid, item_id, transaction_type, amount):
        cursor.execute("SELECT meal_balance, to_go_boxes FROM Students WHERE pid = %s", (pid,))
        student = cursor.fetchone()
        if not student:
            raise Exception("Student not found.")
        balance, to_go_boxes = student

        if transaction_type == "meal swipe" and balance < amount:
            raise Exception("Insufficient balance.")
        if transaction_type == "to-go box checkout" and to_go_boxes >= 3:
            raise Exception("To-go box limit exceeded.")

        # Update balance and boxes
        if transaction_type == "meal swipe":
            cursor.execute("UPDATE Students SET meal_balance = meal_balance - %s WHERE pid = %s", (amount, pid))
        elif transaction_type == "to-go box checkout":
            cursor.execute("UPDATE Students SET to_go_boxes = to_go_boxes + 1 WHERE pid = %s", (pid,))

        # Update menu quantity
        cursor.execute("UPDATE Menu SET quantity = quantity - 1 WHERE item_id = %s", (item_id,))

        # Insert into Transactions and DiningHistory
        cursor.execute(
            "INSERT INTO Transactions (student_id, item_id, transaction_type, transaction_date, amount) VALUES (%s, %s, %s, CURDATE(), %s)",
            (pid, item_id, transaction_type, amount)
        )
        cursor.execute(
            "INSERT INTO DiningHistory (student_id, transaction_date, transaction_type, item_id, meal_type) VALUES (%s, CURDATE(), %s, %s, %s)",
            (pid, transaction_type, item_id, "breakfast")  # Adjust meal_type dynamically if needed
        )
        self.db.commit()

    def get_all_students(self):
        query = "SELECT pid, CONCAT(first_name, ' ', last_name), meal_balance, to_go_boxes FROM Students"
        cursor.execute(query)
        return cursor.fetchall()

    def get_all_menu_items(self):
        query = "SELECT item_id, item_name, quantity, price, meal_type FROM Menu"
        cursor.execute(query)
        return cursor.fetchall()

    def get_all_transactions(self):
        query = """
        SELECT transaction_id, student_id, item_id, transaction_type, amount
        FROM Transactions
        """
        cursor.execute(query)
        return cursor.fetchall()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
