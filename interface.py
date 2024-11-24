from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QStackedWidget, QHBoxLayout,QCalendarWidget, QComboBox
)
from PyQt5.QtCore import Qt, QDate
import pymysql
import sys
import hashlib

db = pymysql.connect(
    host='localhost',
    user='rysch01',
    password='SQLP4ssword1!',
    database='cafeteria',
)
cursor = db.cursor()

class LoginPage(QWidget):
    global cursor
    def __init__(self, switch_to_admin, switch_to_student, switch_to_register):
        super().__init__()
        self.switch_to_admin = switch_to_admin
        self.switch_to_student = switch_to_student
        self.switch_to_register = switch_to_register
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

        self.error_display = QTextEdit(self)
        self.error_display.setReadOnly(True)
        self.error_display.setStyleSheet('color: red;')
        layout.addWidget(self.error_display)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.switch_to_register_button = QPushButton('Register?', self)
        self.switch_to_register_button.clicked.connect(self.switch_to_register)
        layout.addWidget(self.switch_to_register_button)


        self.setLayout(layout)

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


class RegistrationView(QWidget):
    global cursor
    global db
    def __init__(self, switch_to_login, backend):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.backend = backend
        self.initUI()
    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel('Registration', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title_label)
        
        self.pid_input = QLineEdit(self)
        self.pid_input.setPlaceholderText('Enter 9 Digit PID Number')
        layout.addWidget(self.pid_input)

        self.first_input = QLineEdit(self)
        self.first_input.setPlaceholderText('First Name')
        layout.addWidget(self.first_input)

        self.last_input = QLineEdit(self)
        self.last_input.setPlaceholderText('Last Name')
        layout.addWidget(self.last_input)

        self.password_input1 = QLineEdit(self)
        self.password_input1.setPlaceholderText('Enter Password (9-24 characters)')
        self.password_input1.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input1)

        self.password_input2 = QLineEdit(self)
        self.password_input2.setPlaceholderText('Re-enter Password')
        self.password_input2.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input2)


        self.error_display = QTextEdit(self)
        self.error_display.setReadOnly(True)
        self.error_display.setStyleSheet('color: red;')
        layout.addWidget(self.error_display)


        self.registration_button = QPushButton('Register', self)
        self.registration_button.clicked.connect(self.handle_registration)
        layout.addWidget(self.registration_button)



      

        logout_button = QPushButton("Login?")
        logout_button.clicked.connect(self.switch_to_login)
        layout.addWidget(logout_button)

        self.setLayout(layout)

    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_registration(self):
        self.error_display.setStyleSheet('color: red;')

        entered_pid=self.pid_input.text()
        entered_first = self.first_input.text()
        entered_last = self.last_input.text()
        entered_password1 = self.password_input1.text()
        entered_password2 = self.password_input2.text()

                
        if entered_pid=='' or not entered_pid.isdigit() or len(entered_pid) != 9: # (check 9 digit num)
            self.error_display.setText("Error: Enter valid PID.")

        elif entered_first=='' or not entered_first.isalpha(): # check not empty, only letters (no num, whitespace)
            self.error_display.setText('Error: Enter valid First Name')
        elif entered_last=='' or not entered_last.isalpha(): # check not empty, only letters (no num, whitespace)
            self.error_display.setText('Error: Enter valid Last Name')
        elif entered_password1=='' or len(entered_password1) > 24 or len(entered_password1) < 8:  # checks empty, add other check for validity
            self.error_display.setText('Error: Enter valid password; must be between 8 and 24 characters')
        elif entered_password2 != entered_password1: # triggers if first valid but second doesn't match
            self.error_display.setText('Error: Passwords do Not Match')
        else: # means all valid
            self.error_display.clear()

            # # Check if PID in use
            cursor.execute('SELECT * FROM Students S WHERE S.pid=%s', entered_pid)
            result = cursor.fetchall()
            try:
                result[0][0] # if returns a result, it's being used
                self.error_display.setText('Error: PID Already in Use')
            except: # may be a bad idea as any error will allow it to continue, but I think the only error for this would be an index error meaning that there's no PID in use
                self.error_display.clear()
                new_user_details = (entered_pid, entered_first.title(), entered_last.title(), self.hash_password(entered_password1))
                print(new_user_details)
                cursor.execute('INSERT INTO Students (pid, first_name, last_name, password_hash) VALUES (%s, %s, %s, %s);', new_user_details)
                db.commit()
                self.error_display.setStyleSheet('color: green;')
                self.error_display.setText('Registration Successful. Please return to the login page to sign in.')
        



class AdminView(QWidget):
    global cursor
    def __init__(self, switch_to_login, switch_to_manage_students, switch_to_view_transactions, backend):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.switch_to_manage_students = switch_to_manage_students
        self.switch_to_view_transactions = switch_to_view_transactions
        self.backend = backend
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()


        # layout.addWidget(QLabel(f"Name: {student_name}"))
        # layout.addWidget(QLabel(f"PID: {pid}"))

        self.title_label = QLabel('Admin Dashboard', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title_label)
        

        manage_students_button = QPushButton("Manage Students")
        manage_students_button.clicked.connect(self.switch_to_manage_students)
        layout.addWidget(manage_students_button)

        view_transactions_button = QPushButton("View Transactions")
        view_transactions_button.clicked.connect(self.switch_to_view_transactions)
        layout.addWidget(view_transactions_button)

        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.switch_to_login)
        layout.addWidget(logout_button)

        self.setLayout(layout)




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

        cursor.execute('SELECT * FROM Transactions T WHERE T.pid=%s', current_user["pid"])
        result = cursor.fetchall()

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

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(self.selected_date)  # Set today's date
        self.calendar.clicked.connect(self.select_date)
        layout.addWidget(self.calendar)

        self.menu=QTableWidget(self)
        self.menu.setColumnCount(4)
        self.menu.setHorizontalHeaderLabels(['Meal', 'Item', 'Price', 'Calories'])
        layout.addWidget(self.menu)

        self.update_menu_based_on_date(self.selected_date)

        self.payment_history_label = QLabel(f"Payment History", self)
        layout.addWidget(self.payment_history_label)
        self.payment_history=QTableWidget(self)
        self.payment_history.setColumnCount(5)
        self.payment_history.setHorizontalHeaderLabels(['Date', 'Meal', 'Item', 'Price', 'Type'])
        cursor.execute('SELECT * FROM Transactions T LEFT JOIN Menu M ON M.item_id = T.item_id WHERE T.pid = %s', pid)
        result=cursor.fetchall()

        self.payment_history.setRowCount(len(result))
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
        current_user=None
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
    def __init__(self):
        super().__init__()
        self.backend = DatabaseBackend()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cafeteria Database Interface')
        self.setGeometry(480, 480, 1536, 1024)

        self.stacked_widget = QStackedWidget()

        self.login_page = LoginPage(self.show_admin_view, self.show_student_view, self.show_registration_view)
        self.registration_view = RegistrationView(self.show_login_page, self.backend)
        self.admin_view = AdminView(self.show_login_page, self.show_manage_students, self.show_view_transactions, self.backend)
        self.manage_students_page = ManageStudentsPage(self.show_admin_view)
        self.view_transactions_page = ViewTransactionsPage(self.show_admin_view, self.backend)

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.registration_view)
        self.stacked_widget.addWidget(self.admin_view)
        self.stacked_widget.addWidget(self.manage_students_page)
        self.stacked_widget.addWidget(self.view_transactions_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.show_login_page()

    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_registration_view(self):
        self.stacked_widget.setCurrentWidget(self.registration_view)

    def show_admin_view(self):
        self.stacked_widget.setCurrentWidget(self.admin_view)

    def show_manage_students(self):
        self.stacked_widget.setCurrentWidget(self.manage_students_page)

    def show_view_transactions(self):
        self.stacked_widget.setCurrentWidget(self.view_transactions_page)

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
            "INSERT INTO Transactions (pid, item_id, transaction_type, transaction_date) VALUES (%s, %s, %s, CURDATE())",
            (pid, item_id, transaction_type)
        )
        cursor.execute(
            "INSERT INTO DiningHistory (pid, transaction_date, transaction_type, item_id, meal_type) VALUES (%s, CURDATE(), %s, %s, %s)",
            (pid, transaction_type, item_id, "breakfast")  # Adjust meal_type dynamically if needed
        )
        self.db.commit()

    def get_all_students(self):
        query = "SELECT pid, CONCAT(first_name, ' ', last_name), meal_balance, to_go_boxes_remaining FROM Students where role='student'"
        cursor.execute(query)
        return cursor.fetchall()

    def get_all_menu_items(self):
        query = "SELECT item_id, item_name, quantity, price, meal_type FROM Menu"
        cursor.execute(query)
        return cursor.fetchall()

    
    def get_all_transactions(self):
        query = """
        SELECT T.transaction_id, T.pid, T.item_id, T.transaction_type, T.item_id,
               S.first_name, S.last_name, M.item_name, T.transaction_date, M.price From Transactions T left join Students S ON T.pid=S.pid Left Join Menu M on T.item_id=M.item_id
        """


        cursor.execute(query)
        return cursor.fetchall()
    
    def get_transactions_by_pid(self, pid):
        print(pid)
        cursor.execute("""
        SELECT T.transaction_id, T.pid, T.item_id, T.transaction_type, T.item_id,
               S.first_name, S.last_name, M.item_name, T.transaction_date, M.price From Transactions T left join Students S ON T.pid=S.pid Left Join Menu M on T.item_id=M.item_id Where T.pid=%s
        """, (str(pid)))

        return cursor.fetchall()
    
class ManageStudentsPage(QWidget):
    def __init__(self, switch_to_admin):
        super().__init__()
        self.switch_to_admin = switch_to_admin
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("Manage Students")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        pid_label = QLabel("Enter Student PID:")
        layout.addWidget(pid_label)
        self.pid_input = QLineEdit()
        layout.addWidget(self.pid_input)

        add_togo_box_button = QPushButton("Add To-Go Box")
        add_togo_box_button.clicked.connect(self.add_togo_box)
        layout.addWidget(add_togo_box_button)

        add_balance_button = QPushButton("Add Meal Balance")
        add_balance_button.clicked.connect(self.add_balance)
        layout.addWidget(add_balance_button)

        delete_student_button = QPushButton("Delete Student")
        delete_student_button.clicked.connect(self.delete_student)
        layout.addWidget(delete_student_button)

        self.student_action_message = QLabel("")
        layout.addWidget(self.student_action_message)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.switch_to_admin)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def add_togo_box(self):
        pid = self.pid_input.text()
        try:
            cursor.execute("UPDATE Students SET to_go_boxes_remaining = to_go_boxes_remaining + 1 WHERE pid = %s", (pid,))
            if cursor.rowcount == 0:
                self.student_action_message.setText("Error: Student not found.")
            else:
                db.commit()
                self.student_action_message.setText("To-Go Box added successfully!")
        except Exception as e:
            self.student_action_message.setText(f"Error: {e}")

    def add_balance(self):
        pid = self.pid_input.text()
        try:
            balance, ok = QInputDialog.getDouble(self, "Add Balance", "Enter Amount:", 0.0, 0, 1000, 2)
            if ok:
                cursor.execute("UPDATE Students SET meal_balance = meal_balance + %s WHERE pid = %s", (balance, pid))
                if cursor.rowcount == 0:
                    self.student_action_message.setText("Error: Student not found.")
                else:
                    db.commit()
                    self.student_action_message.setText(f"${balance:.2f} added to balance!")
        except Exception as e:
            self.student_action_message.setText(f"Error: {e}")

    def delete_student(self):
        pid = self.pid_input.text()
        try:
            cursor.execute("DELETE FROM Students WHERE pid = %s", (pid,))
            if cursor.rowcount == 0:
                self.student_action_message.setText("Error: Student not found.")
            else:
                db.commit()
                self.student_action_message.setText("Student deleted successfully!")
        except Exception as e:
            self.student_action_message.setText(f"Error: {e}")


class ViewTransactionsPage(QWidget):
    def __init__(self, switch_to_admin, backend):
        super().__init__()
        self.switch_to_admin = switch_to_admin
        self.backend = backend
        self.initUI()

class ViewTransactionsPage(QWidget):
    def __init__(self, switch_to_admin, backend):
        super().__init__()
        self.switch_to_admin = switch_to_admin
        self.backend = backend
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Transaction History")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # Student dropdown
        student_data = self.backend.get_all_students()
        students = ['All Students']
        for sd in student_data:
            students.append(f"{sd[0]} - {sd[1]}")  # Format as "PID - Name"

        self.student_dropdown = QComboBox(self)
        self.student_dropdown.addItems(students)
        self.student_dropdown.currentTextChanged.connect(self.handle_student_selection)
        layout.addWidget(self.student_dropdown)

        # Transaction table
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(7)
        self.transaction_table.setHorizontalHeaderLabels(
            ["Transaction ID", "Date", "PID", "Student Name", "Item Name", "Price", "Type"]
        )
        layout.addWidget(self.transaction_table)

        # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.switch_to_admin)
        layout.addWidget(back_button)

        self.setLayout(layout)

        # Load all transactions by default
        self.load_transactions()

    def load_transactions(self, pid=None):
        print(pid)
        if pid == 'All Students' or pid == '' or pid is None:
            transaction_data = self.backend.get_all_transactions()  # Get all transactions
        else:
            transaction_data = self.backend.get_transactions_by_pid(pid)  # Get transactions for a specific student

        # Clear the table
        self.transaction_table.setRowCount(0)

        # Populate the table
        for row, transaction in enumerate(transaction_data):
            tid = transaction[0]
            tdate = transaction[8]
            pid = transaction[1]
            sname = f"{transaction[5]} {transaction[6]}"
            mname = transaction[9]
            mprice = transaction[7]
            ttype = transaction[3]

            self.transaction_table.insertRow(row)
            self.transaction_table.setItem(row, 0, QTableWidgetItem(str(tid)))
            self.transaction_table.setItem(row, 1, QTableWidgetItem(str(tdate)))
            self.transaction_table.setItem(row, 2, QTableWidgetItem(str(pid)))
            self.transaction_table.setItem(row, 3, QTableWidgetItem(str(sname)))
            self.transaction_table.setItem(row, 4, QTableWidgetItem(str(mname)))
            self.transaction_table.setItem(row, 5, QTableWidgetItem(str(mprice)))
            self.transaction_table.setItem(row, 6, QTableWidgetItem(str(ttype)))

    def handle_student_selection(self, selected_student):
        """
        Handle student selection from the dropdown and filter the table.
        """
        if not selected_student.strip():  # Ignore empty selection
            self.load_transactions()  # Load all transactions
            return

        # Extract PID from the selected entry
        pid = selected_student.split(" - ")[0]
        print(f"Selected Student PID: {pid}")

        # Load transactions for the selected student
        self.load_transactions(pid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
