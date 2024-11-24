import sys
import hashlib
import pymysql
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout,
)
from PyQt5.QtCore import Qt


# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Backend: Database operations
class DatabaseBackend:
    def __init__(self, username, password):
        self.db = None
        self.cursor = None
        try:
            self.db = pymysql.connect(host="localhost", user=username, password=password, database="cafeteria")
            self.cursor = self.db.cursor()
        except Exception as e:
            raise Exception(f"Database connection failed: {e}")

    def validate_login(self, pid, password):
        try:
            hashed_password = hash_password(password)
            query = "SELECT * FROM Students WHERE pid = %s AND password_hash = %s"
            self.cursor.execute(query, (pid, hashed_password))
            result = self.cursor.fetchone()
            return result is not None  # Returns True if credentials match, else False
        except Exception as e:
            raise Exception(f"Login validation failed: {e}")

    def register_user(self, pid, first_name, last_name, password):
        try:
            # Check if PID already exists
            self.cursor.execute("SELECT * FROM Students WHERE pid = %s", (pid,))
            if self.cursor.fetchone():
                raise Exception("PID already exists. Please use a different PID.")

            # Insert new user
            hashed_password = hash_password(password)
            query = "INSERT INTO Students (pid, first_name, last_name, password_hash) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (pid, first_name.title(), last_name.title(), hashed_password))
            self.db.commit()
        except Exception as e:
            raise Exception(f"Registration failed: {e}")


# Frontend: GUI for user interaction
class CafeteriaApp(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.setWindowTitle("Cafeteria System")
        self.setGeometry(100, 100, 400, 300)
        self.backend = backend
        self.current_user = None
        self.setStyleSheet(self.load_styles())

        # Show login screen initially
        self.show_login_screen()

    def load_styles(self):
        return """
            QLabel {
                font-size: 16px;
                font-family: Arial, Helvetica, sans-serif;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            QPushButton {
                font-size: 14px;
                font-family: Arial, Helvetica, sans-serif;
                padding: 8px 15px;
                border: none;
                background-color: #004085; /* Darker blue */
                color: black;
                border-radius: 5px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #002752; /* Even darker blue for hover */
            }
            QWidget {
                background-color: #f5f5f5;
            }
        """

    def show_login_screen(self):
        self.clear_screen()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Cafeteria System Login")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        self.pid_input = QLineEdit()
        self.pid_input.setPlaceholderText("Enter PID")
        layout.addWidget(self.pid_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(login_button)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.show_register_screen)
        button_layout.addWidget(register_button)

        layout.addLayout(button_layout)

        # Set central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_register_screen(self):
        self.clear_screen()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Register for Cafeteria System")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        self.reg_pid_input = QLineEdit()
        self.reg_pid_input.setPlaceholderText("Enter PID")
        layout.addWidget(self.reg_pid_input)

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter First Name")
        layout.addWidget(self.first_name_input)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter Last Name")
        layout.addWidget(self.last_name_input)

        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText("Enter Password")
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_input)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.handle_register)
        layout.addWidget(register_button)

        back_button = QPushButton("Back to Login")
        back_button.clicked.connect(self.show_login_screen)
        layout.addWidget(back_button)

        # Set central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def handle_login(self):
        pid = self.pid_input.text()
        password = self.password_input.text()

        if not pid.isdigit():
            QMessageBox.critical(self, "Error", "PID must be numeric.")
            return

        try:
            if self.backend.validate_login(pid, password):
                self.current_user = pid
                QMessageBox.information(self, "Success", f"Welcome, PID {pid}!")
                self.show_main_screen()
            else:
                QMessageBox.critical(self, "Error", "Invalid PID or password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def handle_register(self):
        pid = self.reg_pid_input.text()
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        password = self.reg_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not pid.isdigit() or len(pid) != 9:
            QMessageBox.critical(self, "Error", "PID must be a 9-digit number.")
            return

        if not first_name.isalpha():
            QMessageBox.critical(self, "Error", "First name must contain only letters.")
            return

        if not last_name.isalpha():
            QMessageBox.critical(self, "Error", "Last name must contain only letters.")
            return

        if len(password) < 8 or len(password) > 24:
            QMessageBox.critical(self, "Error", "Password must be between 8 and 24 characters.")
            return

        if password != confirm_password:
            QMessageBox.critical(self, "Error", "Passwords do not match.")
            return

        try:
            self.backend.register_user(pid, first_name, last_name, password)
            QMessageBox.information(self, "Success", "Registration successful. Please log in.")
            self.show_login_screen()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_main_screen(self):
        self.clear_screen()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        welcome_label = QLabel(f"Welcome to the Cafeteria System, PID {self.current_user}!")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(welcome_label)

        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.show_login_screen)
        layout.addWidget(logout_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def clear_screen(self):
        current_widget = self.centralWidget()
        if current_widget:
            current_widget.deleteLater()


# Run the application
if __name__ == "__main__":
    try:
        # Replace these credentials with actual MySQL username and password
        username = "rysch01"
        password = "SQLP4ssword1!"
        backend = DatabaseBackend(username, password)
    except Exception as e:
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "Fatal Error", str(e))
        sys.exit(1)

    app = QApplication(sys.argv)
    window = CafeteriaApp(backend)
    window.show()
    sys.exit(app.exec_())
