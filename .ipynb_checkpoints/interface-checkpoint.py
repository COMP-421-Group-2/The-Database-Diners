from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QStackedWidget, QHBoxLayout,QCalendarWidget, QComboBox, QSpacerItem, QSizePolicy, QInputDialog, QHeaderView, QCheckBox,
    QScrollArea
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, QDate
import pymysql
import sys
import hashlib

db = pymysql.connect(
    host='localhost',
    user='haleyap',
    password='421SQLpass!',
    database='cafeteria',
)
cursor = db.cursor()
cursor.execute("USE cafeteria")


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

        login_widget = QWidget()
        login_widget.setFixedSize(400, 300)
        login_layout = QVBoxLayout(login_widget)

        self.title_label = QLabel('Login Page', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        login_layout.addWidget(self.title_label)

        self.pid_input = QLineEdit(self)
        self.pid_input.setPlaceholderText('Enter PID')
        login_layout.addWidget(self.pid_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.password_input)

        self.error_display = QTextEdit(self)
        self.error_display.setReadOnly(True)
        self.error_display.setStyleSheet('background: transparent; color: red; border:none;')
        self.error_display.setFixedHeight(30)
        self.error_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        login_layout.addWidget(self.error_display)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)
        login_layout.addWidget(self.login_button)

        self.switch_to_register_button = QPushButton('Register?', self)
        self.switch_to_register_button.clicked.connect(self.switch_to_register)
        login_layout.addWidget(self.switch_to_register_button)

        layout.addWidget(login_widget, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def clear_fields(self):
        """Clear input fields and error messages."""
        self.pid_input.clear()
        self.password_input.clear()
        self.error_display.clear()

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

        registration_widget=QWidget()
        registration_widget.setFixedSize(400, 500) 
        registration_layout=QVBoxLayout(registration_widget)

        self.title_label = QLabel('Registration', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        registration_layout.addWidget(self.title_label)
        
        self.pid_input = QLineEdit(self)
        self.pid_input.setPlaceholderText('Enter 9 Digit PID Number')
        registration_layout.addWidget(self.pid_input)

        self.first_input = QLineEdit(self)
        self.first_input.setPlaceholderText('First Name')
        registration_layout.addWidget(self.first_input)

        self.last_input = QLineEdit(self)
        self.last_input.setPlaceholderText('Last Name')
        registration_layout.addWidget(self.last_input)

        self.password_input1 = QLineEdit(self)
        self.password_input1.setPlaceholderText('Enter Password (9-24 characters)')
        self.password_input1.setEchoMode(QLineEdit.Password)
        registration_layout.addWidget(self.password_input1)

        self.password_input2 = QLineEdit(self)
        self.password_input2.setPlaceholderText('Re-enter Password')
        self.password_input2.setEchoMode(QLineEdit.Password)
        registration_layout.addWidget(self.password_input2)


        self.error_display = QTextEdit(self)
        self.error_display.setReadOnly(True)
        self.error_display.setStyleSheet('color: red; border:none;background: transparent;')
        registration_layout.addWidget(self.error_display)
        self.error_display.setFixedHeight(30)
        self.error_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 

        self.registration_button = QPushButton('Register', self)
        self.registration_button.clicked.connect(self.handle_registration)
        registration_layout.addWidget(self.registration_button)



      

        login_button = QPushButton("Login?")
        login_button.clicked.connect(self.switch_to_login)
        registration_layout.addWidget(login_button)

        layout.addWidget(registration_widget, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_registration(self):
        
        
        self.error_display.setStyleSheet('color: red; border:none;background: transparent;')

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
                cursor.callproc('register_student', new_user_details)
                print('used procedure here')
                db.commit()
                self.error_display.setStyleSheet('background: transparent; color: green; border:none;')
                self.error_display.setText('Registration Successful. Please sign in.')
        



class AdminView(QWidget):
    global cursor

    def __init__(self, switch_to_login, switch_to_manage_students, switch_to_view_transactions, backend, admin_pid, view_transactions_page):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.switch_to_manage_students = switch_to_manage_students
        self.switch_to_view_transactions = switch_to_view_transactions
        self.backend = backend
        self.admin_pid = admin_pid
        self.view_transactions_page = view_transactions_page
        self.admin_name = self.backend.get_student_name(admin_pid)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Admin Header
        admin_header = QVBoxLayout()  # Use a vertical layout for Name and PID
        admin_name_label = QLabel(f"Name: {self.admin_name}")
        admin_name_label.setAlignment(Qt.AlignLeft)
        admin_pid_label = QLabel(f"PID: {self.admin_pid}")
        admin_pid_label.setAlignment(Qt.AlignLeft)
        
        admin_header.addWidget(admin_name_label)
        admin_header.addWidget(admin_pid_label)

        header_widget = QWidget()
        header_widget.setLayout(admin_header)
        layout.addWidget(header_widget)

        # Admin Title
        self.title_label = QLabel('Admin Dashboard', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title_label)

        # Buttons for admin actions in a row
        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout(buttonWidget)  # Use horizontal layout for row arrangement

        manage_students_button = QPushButton("Manage Students")
        manage_students_button.setFixedHeight(50)  # Reduce height
        manage_students_button.setFixedWidth(200)  # Reduce width
        manage_students_button.clicked.connect(self.switch_to_manage_students)
        buttonLayout.addWidget(manage_students_button)

        view_transactions_button = QPushButton("View Transactions")
        view_transactions_button.setFixedHeight(50)  # Reduce height
        view_transactions_button.setFixedWidth(200)  # Reduce width
        view_transactions_button.clicked.connect(self.switch_to_view_transactions)
        buttonLayout.addWidget(view_transactions_button)

        logout_button = QPushButton("Logout")
        logout_button.setFixedHeight(50)  # Reduce height
        logout_button.setFixedWidth(200)  # Reduce width
        logout_button.clicked.connect(self.switch_to_login)
        buttonLayout.addWidget(logout_button)

        buttonLayout.setAlignment(Qt.AlignCenter)  # Center the row of buttons
        layout.addWidget(buttonWidget)

        # Order Placement Section
        self.order_section = self.create_order_section()
        layout.addWidget(self.order_section)

        self.setLayout(layout)



    def create_order_section(self):
        """
        Creates the section for placing an order.
        """
        order_widget = QWidget()
        order_layout = QVBoxLayout(order_widget)

        # Section title
        order_title = QLabel("Place an Order")
        order_title.setAlignment(Qt.AlignCenter)
        order_title.setStyleSheet('font-size: 18px; font-weight: bold;')
        order_layout.addWidget(order_title)

        # Dropdown to select a student
        self.student_dropdown = QComboBox()
        self.populate_student_dropdown()
        order_layout.addWidget(self.student_dropdown)

        self.order_date_picker = QCalendarWidget()
        self.order_date_picker.setGridVisible(True)
        self.order_date_picker.clicked.connect(self.load_menu_for_order)
        order_layout.addWidget(self.order_date_picker)

        # Add to-go box option
        self.togo_checkbox = QCheckBox("Use To-Go Box")
        order_layout.addWidget(self.togo_checkbox)

        self.menu_table = QTableWidget()
        self.menu_table.setColumnCount(6)
        self.menu_table.setHorizontalHeaderLabels(['Item ID', 'Item Name', 'Price', 'Calories', 'Quantity Left', 'Order'])
        order_layout.addWidget(self.menu_table)

        # Place order button
        place_order_button = QPushButton("Place Order")
        place_order_button.setFixedHeight(50)  # Reduce height
        place_order_button.setFixedWidth(200)  # Reduce width
        place_order_button.clicked.connect(self.place_order)
        order_layout.addWidget(place_order_button)

        self.order_status_message = QLabel("")
        order_layout.addWidget(self.order_status_message)

        return order_widget



    def populate_student_dropdown(self):
        """Populate dropdown with all students."""
        students = self.backend.get_all_students()
        for student in students:
            self.student_dropdown.addItem(f"{student[0]} - {student[1]}", student[0])

    def load_menu_for_order(self):
        """
        Dynamically updates the menu table when a date is selected in the calendar.
        """
        selected_date = self.order_date_picker.selectedDate().toString('yyyy-MM-dd')
        self.menu_table.setRowCount(0)  # Clear the table before loading new data

        # Fetch menu items for the selected date
        menu_items = self.backend.get_menu_for_date(selected_date)

        if not menu_items:
            self.order_status_message.setText(f"No menu available for {selected_date}.")
            return

        self.order_status_message.setText("")  # Clear any previous status message
        self.menu_table.setRowCount(len(menu_items))

        # Populate the table with menu items
        for row_idx, item in enumerate(menu_items):
            self.menu_table.setItem(row_idx, 0, QTableWidgetItem(str(item[0])))  # Item ID
            self.menu_table.setItem(row_idx, 1, QTableWidgetItem(item[1]))  # Item Name
            self.menu_table.setItem(row_idx, 2, QTableWidgetItem(f"${item[5]:.2f}"))  # Price
            self.menu_table.setItem(row_idx, 3, QTableWidgetItem(str(item[2])))  # Calories
            self.menu_table.setItem(row_idx, 4, QTableWidgetItem(str(item[6])))  # Quantity Left

            # Add a checkbox for ordering
            checkbox_widget = QCheckBox()
            checkbox_widget.setStyleSheet("margin-left:50%; margin-right:50%;")  # Center checkbox
            self.menu_table.setCellWidget(row_idx, 5, checkbox_widget)



    def place_order(self):
        """
        Places an order for the selected student.
        """
        selected_student = self.student_dropdown.currentData()
        if not selected_student:
            self.order_status_message.setText("Error: Please select a student.")
            return

        # Get student info
        student_info = self.backend.get_user_info(selected_student)
        if not student_info:
            self.order_status_message.setText("Error: Invalid Student.")
            return

        # Check if the student wants to use a to-go box
        use_togo_box = self.togo_checkbox.isChecked()
        if use_togo_box and student_info[4] <= 0:  # Check to_go_boxes_remaining
            self.order_status_message.setText("Error: No to-go boxes remaining.")
            return

        total_cost = 0
        ordered_items = []  # List to hold ordered items
        for row_idx in range(self.menu_table.rowCount()):
            item_id = self.menu_table.item(row_idx, 0).text()
            item_name = self.menu_table.item(row_idx, 1).text()
            price = float(self.menu_table.item(row_idx, 2).text().replace('$', ''))
            available_quantity = int(self.menu_table.item(row_idx, 4).text())
            checkbox_widget = self.menu_table.cellWidget(row_idx, 5)

            if checkbox_widget and checkbox_widget.isChecked():
                if available_quantity <= 0:
                    self.order_status_message.setText(f"Error: {item_name} is out of stock.")
                    return

                total_cost += price
                ordered_items.append(item_id)

        if total_cost == 0:
            self.order_status_message.setText("Error: No items selected.")
            return

        # Check if the student has enough balance
        if student_info[3] < total_cost:
            self.order_status_message.setText("Error: Insufficient balance.")
            return

        try:
            # Update student balance
            cursor.execute("UPDATE Students SET meal_balance = meal_balance - %s WHERE pid = %s", (total_cost, selected_student))

            # Update to-go boxes if the option is selected
            if use_togo_box:
                cursor.execute("UPDATE Students SET to_go_boxes_remaining = to_go_boxes_remaining - 1 WHERE pid = %s", (selected_student,))

            # Update menu item quantities and insert transactions
            for item_id in ordered_items:
                transaction_type = "to-go" if use_togo_box else "dine-in"
                cursor.execute("UPDATE Menu SET quantity = quantity - 1 WHERE item_id = %s", (item_id,))
                cursor.execute(
                    "INSERT INTO Transactions (pid, item_id, transaction_type, transaction_date) VALUES (%s, %s, %s, %s)",
                    (selected_student, item_id, transaction_type, QDate.currentDate().toString('yyyy-MM-dd'))
                )

            # Insert a separate transaction for the to-go box if used
            if use_togo_box:
                cursor.execute(
                    "INSERT INTO Transactions (pid, item_id, transaction_type, transaction_date) VALUES (%s, %s, %s, %s)",
                    (selected_student, -1, "to-go", QDate.currentDate().toString('yyyy-MM-dd'))
                )

            db.commit()
            self.order_status_message.setStyleSheet("color: green;")
            self.order_status_message.setText("Order placed successfully!")
            self.load_menu_for_order()  # Refresh the menu table

            # Refresh the transaction table
            self.view_transactions_page.reload_transactions()
        except Exception as e:
            self.order_status_message.setStyleSheet("color: red;")
            self.order_status_message.setText(f"Error: {e}")


    def place_order(self):
        """
        Places an order for the selected student.
        """
        selected_student = self.student_dropdown.currentData()
        if not selected_student:
            self.order_status_message.setText("Error: Please select a student.")
            return

        # Get student info
        student_info = self.backend.get_user_info(selected_student)
        if not student_info:
            self.order_status_message.setText("Error: Invalid Student.")
            return

        # Check if the student wants to use a to-go box
        use_togo_box = self.togo_checkbox.isChecked()
        if use_togo_box and student_info[4] <= 0:  # Check to_go_boxes_remaining
            self.order_status_message.setText("Error: No to-go boxes remaining.")
            return

        total_cost = 0
        ordered_items = []  # List to hold ordered items

        # Iterate through menu items to identify selected items
        for row_idx in range(self.menu_table.rowCount()):
            item_id = self.menu_table.item(row_idx, 0).text()
            item_name = self.menu_table.item(row_idx, 1).text()
            price = float(self.menu_table.item(row_idx, 2).text().replace('$', ''))
            available_quantity = int(self.menu_table.item(row_idx, 4).text())  # Quantity Left
            checkbox_widget = self.menu_table.cellWidget(row_idx, 5)

            # Check if the item is selected using the checkbox
            if checkbox_widget and checkbox_widget.isChecked():
                if available_quantity <= 0:
                    self.order_status_message.setText(f"Error: {item_name} is out of stock.")
                    return

                # Add to total cost and record the item
                total_cost += price
                ordered_items.append(item_id)

        # Validate if any items were selected
        if not ordered_items:
            self.order_status_message.setText("Error: No items selected.")
            return

        # Check if the student has enough balance
        if student_info[3] < total_cost:
            self.order_status_message.setText("Error: Insufficient balance.")
            return

        try:
            # Update student balance
            cursor.execute("UPDATE Students SET meal_balance = meal_balance - %s WHERE pid = %s", (total_cost, selected_student))

            # Update to-go boxes if the option is selected
            if use_togo_box:
                cursor.execute("UPDATE Students SET to_go_boxes_remaining = to_go_boxes_remaining - 1 WHERE pid = %s", (selected_student,))

            # Update menu item quantities and insert transactions
            for item_id in ordered_items:
                transaction_type = "to-go" if use_togo_box else "dine-in"
                cursor.execute("UPDATE Menu SET quantity = quantity - 1 WHERE item_id = %s", (item_id,))
                cursor.execute(
                    "INSERT INTO Transactions (pid, item_id, transaction_type, transaction_date) VALUES (%s, %s, %s, %s)",
                    (selected_student, item_id, transaction_type, QDate.currentDate().toString('yyyy-MM-dd'))
                )

            # Insert a separate transaction for the to-go box if used
            if use_togo_box:
                cursor.execute(
                    "INSERT INTO Transactions (pid, item_id, transaction_type, transaction_date) VALUES (%s, %s, %s, %s)",
                    (selected_student, -1, "to-go", QDate.currentDate().toString('yyyy-MM-dd'))
                )

            db.commit()
            self.order_status_message.setStyleSheet("color: green;")
            self.order_status_message.setText("Order placed successfully!")
            self.load_menu_for_order()  # Refresh the menu table
        except Exception as e:
            self.order_status_message.setStyleSheet("color: red;")
            self.order_status_message.setText(f"Error: {e}")





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
        main_layout = QVBoxLayout()
        self.title_label = QLabel('Student Dashboard', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        main_layout.addWidget(self.title_label)
        
        header=QHBoxLayout()


       
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


        headerL=QVBoxLayout()
        headerL.addWidget(QLabel(f"Name: {student_name}"))
        headerL.addWidget(QLabel(f"PID: {pid}"))
        
        headerR=QVBoxLayout()
        ab_label=QLabel(f"Account Balance: ${account_balance:.2f}")
        ab_label.setAlignment(Qt.AlignRight)
        tg_label=QLabel(f"To-Go Boxes Available: {togo_boxes}")
        tg_label.setAlignment(Qt.AlignRight)

        headerR.addWidget(ab_label)
        headerR.addWidget(tg_label)



        left_widget = QWidget()
        left_widget.setLayout(headerL)
        right_widget = QWidget()
        right_widget.setLayout(headerR)
        header.addWidget(left_widget)
        header.addWidget(right_widget)

        menu_layout=QVBoxLayout()
        
        # self.date_label = QLabel(f"Menu for {self.selected_date.toString('yyyy-MM-dd')}", self)
        self.date_label = QLabel("Daily Menu", self)
        self.date_label.setStyleSheet('font-size: 20px; font-weight: bold;')

        menu_layout.addWidget(self.date_label)

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(self.selected_date)  # Set today's date
        self.calendar.clicked.connect(self.select_date)
        menu_layout.addWidget(self.calendar)

        self.menu=QTableWidget(self)
        self.menu.setColumnCount(5)
        self.menu.setHorizontalHeaderLabels(['Meal', 'Item', 'Price', 'Calories', 'Quantity'])
        menu_layout.addWidget(self.menu)

        self.update_menu_based_on_date(self.selected_date)

        payment_layout=QVBoxLayout()

        self.payment_history_label = QLabel(f"Personal Payment History", self)
        self.payment_history_label.setStyleSheet('font-size: 20px; font-weight: bold;')

        payment_layout.addWidget(self.payment_history_label)
        self.payment_history=QTableWidget(self)
        self.payment_history.setColumnCount(5)
        self.payment_history.setHorizontalHeaderLabels(['Date', 'Meal', 'Item', 'Price', 'Type'])
        cursor.execute('SELECT * FROM Transactions T LEFT JOIN Menu M ON M.item_id = T.item_id WHERE T.pid = %s', pid)
        result=cursor.fetchall()

        self.payment_history.setRowCount(len(result))
        for ri, rdata in enumerate(result):
            self.payment_history.setItem(ri, 0, QTableWidgetItem(str(rdata[4])))
            self.payment_history.setItem(ri, 1, QTableWidgetItem(str(rdata[8])))

            temp=str(rdata[6])
            print(temp)
            temp= QTableWidgetItem(temp)
            self.payment_history.setItem(ri, 2,temp)
            self.payment_history.setItem(ri, 3, QTableWidgetItem(str(rdata[10])))
            self.payment_history.setItem(ri, 4, QTableWidgetItem(str(rdata[3])))

        payment_layout.addWidget(self.payment_history)


        # Logout button
        self.logout_button = QPushButton('Logout', self)
        self.logout_button.clicked.connect(self.switch_to_login)
        current_user=None

        body=QHBoxLayout()
        spacer = QWidget()
        spacer.setFixedWidth(10)
        body.addWidget(spacer)
        body.addLayout(payment_layout)
        body.addWidget(spacer)
        body.addLayout(menu_layout)
        body.addWidget(spacer)

        main_layout.addLayout(header)
        main_layout.addLayout(body)
        main_layout.addWidget(self.logout_button)

        self.setLayout(main_layout)

    def select_date(self, date):
        """
        Update the selected date when the user clicks on a date in the calendar.
        """
        self.selected_date = date
        # self.date_label.setText(f"Menu for {self.selected_date.toString('yyyy-MM-dd')}")
        self.date_label = QLabel("Daily Menu", self)
        self.update_menu_based_on_date(self.selected_date)

    def update_menu_based_on_date(self, date):
        """
        Query and print today's menu based on the selected date.
        """
        # Clear rows
        self.menu.setRowCount(0)
        cursor.execute('SELECT * FROM Menu M WHERE available_date=%s', date.toString('yyyy-MM-dd'))
        result = cursor.fetchall()
        print(result)

        meal = {'breakfast': 0, 'lunch': 1, 'dinner': 2}
        result = sorted(result, key=lambda x: meal.get(x[3], 3))  # Default to 3 for unknown types

        # 'Date', 'Meal', 'Item', 'Price', 'Type'
        self.menu.setRowCount(len(result))
        # go through the each row and column data
        for ri, rdata in enumerate(result):
            print(rdata)
            
            self.menu.setItem(ri, 0, QTableWidgetItem(str(rdata[3])))
            self.menu.setItem(ri, 1, QTableWidgetItem(str(rdata[1])))
            self.menu.setItem(ri, 2, QTableWidgetItem(str(rdata[5])))
            self.menu.setItem(ri, 3, QTableWidgetItem(str(rdata[2])))
            self.menu.setItem(ri, 4, QTableWidgetItem(str(rdata[6])))


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
        self.admin_pid = None  # Store the PID of the logged-in admin
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cafeteria Database Interface')
        self.setGeometry(480, 480, 1536, 1024)

        self.stacked_widget = QStackedWidget()

        self.login_page = LoginPage(self.handle_admin_login, self.show_student_view, self.show_registration_view)
        self.registration_view = RegistrationView(self.show_login_page, self.backend)
        self.manage_students_page = ManageStudentsPage(self.show_admin_view)
        self.view_transactions_page = ViewTransactionsPage(self.show_admin_view, self.backend)

        # Add views to the stacked widget
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.registration_view)
        self.stacked_widget.addWidget(self.manage_students_page)
        self.stacked_widget.addWidget(self.view_transactions_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.show_login_page()

    def show_login_page(self):
        self.login_page.clear_fields()  # Clear fields when showing the login page
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_registration_view(self):
        self.stacked_widget.setCurrentWidget(self.registration_view)

    def handle_admin_login(self):
        # Retrieve the PID from the login page
        admin_pid = self.login_page.pid_input.text()
        self.admin_pid = admin_pid  # Save the PID for the logged-in admin
        self.show_admin_view()

    def show_admin_view(self):
        # Ensure admin_pid is passed to the AdminView
        self.admin_view = AdminView(
            self.show_login_page,
            self.show_manage_students,
            self.show_view_transactions,
            self.backend,
            self.admin_pid,
            self.view_transactions_page  # Pass this instance
        )
        self.stacked_widget.addWidget(self.admin_view)
        self.stacked_widget.setCurrentWidget(self.admin_view)


    def show_manage_students(self):
        self.manage_students_page.clear_fields()
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
    
    def get_menu_for_date(self, date, meal_type=None):
        if meal_type:
            query = "SELECT * FROM Menu WHERE available_date = %s AND meal_type = %s"
            cursor.execute(query, (date, meal_type))
        else:
            query = "SELECT * FROM Menu WHERE available_date = %s"
            cursor.execute(query, (date,))
        return cursor.fetchall()


    def process_transaction(self, pid, item_id, transaction_type, amount):
        cursor.execute("SELECT meal_balance, to_go_boxes FROM Students WHERE pid = %s", (pid,))
        student = cursor.fetchone()
        if not student:
            raise Exception("Student not found.")
        balance, to_go_boxes = student

        if transaction_type == "dine-in" and balance < amount:
            raise Exception("Insufficient balance.")
        if transaction_type == "to-go" and to_go_boxes >= 3:
            raise Exception("To-go box limit exceeded.")

        # Update balance and boxes
        if transaction_type == "dine-in":
            cursor.execute("UPDATE Students SET meal_balance = meal_balance - %s WHERE pid = %s", (amount, pid))
        elif transaction_type == "to-go":
            cursor.execute("UPDATE Students SET to_go_boxes = to_go_boxes + 1 WHERE pid = %s", (pid,))

        # Update menu quantity
        # cursor.execute("UPDATE Menu SET quantity = quantity - 1 WHERE item_id = %s", (item_id,))

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
        query = "SELECT item_id, item_name, price, meal_type, quantity FROM Menu"
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

        # Scrollable area for the students table
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Table to display students
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(5)
        self.students_table.setHorizontalHeaderLabels(
            ["PID", "Name", "Last Purchase Date", "Meal Balance", "To-Go Boxes Remaining"]
        )
        self.students_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)  # Dynamically adjust column widths
        self.students_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Add vertical scrolling
        self.students_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Add horizontal scrolling

        # Embed the table in the scroll area
        scroll_area.setWidget(self.students_table)
        layout.addWidget(scroll_area)

        # Populate the students table
        self.load_students_data()

        # Dropdown to select a student
        pid_label = QLabel("Select a Student:")
        layout.addWidget(pid_label)
        self.student_dropdown = QComboBox()
        self.student_dropdown.addItem("Select a student")  # Placeholder item
        layout.addWidget(self.student_dropdown)
        self.populate_student_dropdown()

        add_togo_box_button = QPushButton("Add To-Go Box")
        add_togo_box_button.setFixedHeight(50)  # Reduce height
        add_togo_box_button.setFixedWidth(200)  # Reduce width
        add_togo_box_button.clicked.connect(self.add_togo_box)
        layout.addWidget(add_togo_box_button)

        add_balance_button = QPushButton("Add Meal Balance")
        add_balance_button.setFixedHeight(50)  # Reduce height
        add_balance_button.setFixedWidth(200)  # Reduce width
        add_balance_button.clicked.connect(self.add_balance)
        layout.addWidget(add_balance_button)

        delete_student_button = QPushButton("Delete Student")
        delete_student_button.setFixedHeight(50)  # Reduce height
        delete_student_button.setFixedWidth(200)  # Reduce width
        delete_student_button.clicked.connect(self.delete_student)
        layout.addWidget(delete_student_button)

        self.student_action_message = QLabel("")
        layout.addWidget(self.student_action_message)

        back_button = QPushButton("Back")
        back_button.setFixedHeight(50)  # Reduce height
        back_button.setFixedWidth(200)  # Reduce width
        back_button.clicked.connect(self.back_to_admin)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def load_students_data(self):
        """Fetch and populate the table with student data."""
        query = """
        SELECT 
            S.pid, 
            CONCAT(S.first_name, ' ', S.last_name) AS name, 
            MAX(T.transaction_date) AS last_purchase_date, 
            S.meal_balance, 
            S.to_go_boxes_remaining
        FROM Students S
        LEFT JOIN Transactions T ON S.pid = T.pid
        WHERE S.role = 'student'
        GROUP BY S.pid
        ORDER BY S.pid;
        """
        cursor.execute(query)
        students = cursor.fetchall()

        self.students_table.setRowCount(len(students))
        self.students_table.horizontalHeader().setStretchLastSection(True)  # Stretch last column

        for row_idx, student in enumerate(students):
            for col_idx, value in enumerate(student):
                self.students_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value is not None else "N/A"))

        self.students_table.resizeColumnsToContents()  # Resize columns to fit content dynamically
        self.students_table.resizeRowsToContents()  # Resize rows to fit content dynamically


    def populate_student_dropdown(self):
        """Fetch and populate the dropdown with students."""
        query = """
        SELECT pid, CONCAT(first_name, ' ', last_name) AS name
        FROM Students
        WHERE role = 'student'
        ORDER BY pid;
        """
        cursor.execute(query)
        students = cursor.fetchall()

        # Populate dropdown
        for student in students:
            pid, name = student
            self.student_dropdown.addItem(f"{pid} - {name}", pid)

    def get_selected_pid(self):
        """Extract the selected PID from the dropdown."""
        index = self.student_dropdown.currentIndex()
        if index <= 0:  # Placeholder or no selection
            self.student_action_message.setText("Error: Please select a valid student.")
            return None
        return self.student_dropdown.itemData(index)

    def clear_fields(self):
        """Clear input fields and messages."""
        self.student_dropdown.setCurrentIndex(0)  # Reset dropdown to placeholder
        self.student_action_message.setText("")
        self.students_table.clearContents()
        self.load_students_data()

    def back_to_admin(self):
        """Handle navigation back to the admin view."""
        self.clear_fields()  # Clear fields and reload data before leaving the page
        self.switch_to_admin()

    def add_togo_box(self):
        pid = self.get_selected_pid()
        if pid is None:
            return

        try:
            cursor.execute("UPDATE Students SET to_go_boxes_remaining = to_go_boxes_remaining + 1 WHERE pid = %s", (pid,))
            if cursor.rowcount == 0:
                self.student_action_message.setText("Error: Student not found.")
            else:
                db.commit()
                self.student_action_message.setText("To-Go Box added successfully!")
                self.load_students_data()  # Refresh the table
        except Exception as e:
            self.student_action_message.setText(f"Error: {e}")

    def add_balance(self):
        pid = self.get_selected_pid()
        if pid is None:
            return

        try:
            # Open input dialog to get the balance amount
            amount, ok = QInputDialog.getDouble(self, "Add Balance", "Enter Amount:", 0.0, 0, 10000, 2)
            if ok:  # If user clicked "OK"
                cursor.execute("UPDATE Students SET meal_balance = meal_balance + %s WHERE pid = %s", (amount, pid))
                if cursor.rowcount == 0:
                    self.student_action_message.setText("Error: Student not found.")
                else:
                    db.commit()
                    self.student_action_message.setText(f"${amount:.2f} added to the balance of PID {pid}.")
                    self.load_students_data()  # Refresh the table
        except Exception as e:
            self.student_action_message.setText(f"Error: {e}")

    def delete_student(self):
        pid = self.get_selected_pid()
        if pid is None:
            return

        try:
            # Delete transactions associated with the student
            cursor.execute("DELETE FROM Transactions WHERE pid = %s", (pid,))
            db.commit()  # Commit the transaction deletion first

            # Delete the student
            cursor.execute("DELETE FROM Students WHERE pid = %s", (pid,))
            if cursor.rowcount == 0:
                self.student_action_message.setText("Error: Student not found.")
            else:
                db.commit()
                self.student_action_message.setText(f"Student with PID {pid} deleted successfully.")
                self.load_students_data()  # Refresh the table
        except Exception as e:
            self.student_action_message.setText(f"Error: {e}")



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


    def reload_transactions(self):
        """
        Reload the transactions for the currently selected student or all students.
        """
        current_selection = self.student_dropdown.currentText()
        if current_selection == 'All Students' or not current_selection.strip():
            self.load_transactions()
        else:
            pid = current_selection.split(" - ")[0]
            self.load_transactions(pid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())