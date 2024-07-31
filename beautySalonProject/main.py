import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, \
    QTimeEdit, QMessageBox
from PyQt6.QtCore import QDate, QTime
from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi
from sqlalchemy.orm import Session
from database_setup import SessionLocal, User, Artist, Service, Appointment, Availability
from database_setup import update_service_names, delete_all_users, delete_all_data
from datetime import datetime, timedelta


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        try:
            loadUi("main_window.ui", self)
        except Exception as e:
            print(f"Error loading UI: {e}")
            sys.exit(1)

        # Load images into labels
        self.load_images()

        # Connect buttons to their respective functions
        self.cosmeticsBtn.clicked.connect(self.show_cosmetics)
        self.nailsBtn.clicked.connect(self.show_nails)
        self.hairBtn.clicked.connect(self.show_hair)
        self.meetUsBtn.clicked.connect(self.show_team_window)
        self.productsBtn.clicked.connect(self.show_products_window)
        self.pricesBtn.clicked.connect(self.show_prices_window)
        self.apptBtn.clicked.connect(self.book_appointment)

        self.setStyleSheet("QMainWindow {"
                           "background-image: url(static/logo3.jpg);"
                           "background-repeat: no-repeat;"
                           "background-position: center"
                           "}")

    def load_images(self):
        # Set the images for labels with appropriate paths
        self.set_label_pixmap('static/IMG-20240730-WA0109.jpg', self.findChild(QLabel, 'cosmetics_label'))
        self.set_label_pixmap('static/IMG-20240730-WA0112.jpg', self.findChild(QLabel, 'nails_label'))
        self.set_label_pixmap('static/IMG-20240730-WA0110.jpg', self.findChild(QLabel, 'hair_label'))

    def set_label_pixmap(self, image_path, label):
        if label is not None:
            pixmap = QPixmap(image_path)
            label.setPixmap(pixmap.scaled(label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                          QtCore.Qt.TransformationMode.SmoothTransformation))
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        else:
            print(f"Label not found for path: {image_path}")

    def show_cosmetics(self):
        print("Show cosmetics")

    def show_nails(self):
        print("Show nails")

    def show_hair(self):
        print("Show hair")

    def show_team_window(self):
        self.team_window = MeetTheTeam()  # Create instance of MeetTheTeam
        self.team_window.exec()  # Use exec() to show the dialog

    def show_products_window(self):
        print("Show products window")

    def show_prices_window(self):
        print("Show prices window")

    def book_appointment(self):
        # Open the appointment dialog
        self.appt_window = AppointmentDialog()
        self.appt_window.exec()  # Show as modal dialog


BUFFER_PERIOD = timedelta(hours=2)


class AppointmentDialog(QDialog):
    def __init__(self, parent=None):
        super(AppointmentDialog, self).__init__(parent)
        loadUi("appointment_dialog.ui", self)  # Load the UI file

        # Initialize widgets
        self.categoryComboBox = self.findChild(QComboBox, 'categoryComboBox')
        self.serviceComboBox = self.findChild(QComboBox, 'serviceComboBox')
        self.artistComboBox = self.findChild(QComboBox, 'artistComboBox')
        self.nameLineEdit = self.findChild(QLineEdit, 'nameLineEdit')
        self.phoneLineEdit = self.findChild(QLineEdit, 'phoneLineEdit')
        self.dateEdit = self.findChild(QDateEdit, 'dateEdit')
        self.timeEdit = self.findChild(QTimeEdit, 'timeEdit')
        self.submitButton = self.findChild(QPushButton, 'submitButton')
        self.cancelBtn = self.findChild(QPushButton, 'cancelBtn')

        # Set date to not allow dates before 2024
        self.dateEdit.setMinimumDate(QDate(2024, 1, 1))
        self.dateEdit.setDate(QDate.currentDate())

        # Restrict time selection between 08:00 and 19:00
        self.timeEdit.setMinimumTime(QTime(8, 0))
        self.timeEdit.setMaximumTime(QTime(19, 0))

        # Connect signals
        self.categoryComboBox.currentIndexChanged.connect(self.update_services)
        self.serviceComboBox.currentIndexChanged.connect(self.update_artists)
        self.submitButton.clicked.connect(self.book_appointment)
        self.cancelBtn.clicked.connect(self.close)

        # Populate categories
        self.populate_categories()

        self.setStyleSheet("QDialog {"
                           "background-image: url(static/logo3.jpg);"
                           "background-repeat: no-repeat;"
                           "background-position: center;"
                           "}")

    def populate_categories(self):
        # Add categories to the categoryComboBox
        self.categoryComboBox.addItems(['Nails', 'Hair', 'Cosmetics'])

    def update_services(self):
        self.serviceComboBox.clear()
        selected_category = self.categoryComboBox.currentText().lower()

        # Fetch services from the database based on category
        services = self.get_services_by_category(selected_category)

        # Use a set to ensure unique services
        unique_services = set()
        for service in services:
            unique_services.add(service.name)

        # Add unique services to the serviceComboBox
        self.serviceComboBox.addItems(list(unique_services))

        # Update artists based on new service selection
        self.update_artists()

    def get_services_by_category(self, category):
        db = SessionLocal()
        services = db.query(Service).filter(Service.category == category).all()
        db.close()
        return services

    def update_artists(self):
        self.artistComboBox.clear()
        selected_category = self.categoryComboBox.currentText().lower()
        valid_artists = {
            'nails': ['Roxana', 'Maria'],
            'hair': ['Roxana', 'Maria', 'Daria'],
            'cosmetics': ['Eva']
        }

        artists = valid_artists.get(selected_category, [])
        self.artistComboBox.addItems(artists)

    def book_appointment(self):
        user_name = self.nameLineEdit.text()
        user_phone = self.phoneLineEdit.text()
        service_name = self.serviceComboBox.currentText()
        artist_name = self.artistComboBox.currentText()
        appointment_date = self.dateEdit.date().toPyDate()
        appointment_time = self.timeEdit.time().toPyTime()

        # Validate input fields
        if not user_name or not user_phone:
            QMessageBox.warning(self, "Input Error", "Please fill in both Name and Phone fields.")
            return

        # Validate name and phone number
        if len(user_name) < 4 or not user_name.isalpha():
            QMessageBox.warning(self, "Input Error", "Name must be more than 3 letters and cannot contain numbers.")
            return
        if not (user_phone.isdigit() and len(user_phone) == 10):
            QMessageBox.warning(self, "Input Error", "Phone number must be exactly 10 digits.")
            return

        db = SessionLocal()

        # Fetch service and artist
        service = db.query(Service).filter_by(name=service_name).first()
        artist = db.query(Artist).filter_by(name=artist_name).first()

        if not service or not artist:
            QMessageBox.warning(self, "Booking Error", "Service or Artist not found.")
            db.close()
            return

        # Calculate the start and end time of the appointment
        start_datetime = datetime.combine(appointment_date, appointment_time)
        end_datetime = start_datetime + timedelta(minutes=119)  # Block for 1 hour and 59 minutes

        # Check for conflicting appointments with a 1 hour and 59 minutes block period
        conflicting_appointments = db.query(Appointment).filter_by(
            artist_id=artist.artist_id,
            appointment_date=appointment_date
        ).all()

        for appt in conflicting_appointments:
            appt_start_datetime = datetime.combine(appt.appointment_date, appt.appointment_time)
            appt_end_datetime = appt_start_datetime + timedelta(
                minutes=119)  # Assume existing appointments are also 1 hour and 59 minutes blocks

            # Check for overlap
            if not (end_datetime <= appt_start_datetime or start_datetime >= appt_end_datetime):
                QMessageBox.warning(self, "Booking Error", "The artist is not available during the selected time.")
                db.close()
                return

        # Fetch or create user if no conflicts
        user = db.query(User).filter_by(name=user_name, phone_number=user_phone).first()
        if not user:
            user = User(name=user_name, phone_number=user_phone)
            db.add(user)
            db.commit()  # Commit to save user details

        # Create and save the new appointment
        new_appt = Appointment(
            user_id=user.user_id,
            artist_id=artist.artist_id,
            service_id=service.service_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )
        db.add(new_appt)
        db.commit()
        QMessageBox.information(self, "Success", "Appointment booked successfully.")

        db.close()
        self.close()


class MeetTheTeam(QDialog):
    def __init__(self):
        super(MeetTheTeam, self).__init__()
        try:
            loadUi("meet_the_team.ui", self)
        except Exception as e:
            print(f"Error loading UI: {e}")
            sys.exit(1)

        # Set background color
        self.setStyleSheet("QDialog {"
                           "background-color: black;"
                           "}")

        # Connect buttons to their respective functions
        self.backBtn.clicked.connect(self.close)
        self.bookApptBtn.clicked.connect(self.openAppointmentDialog)

    def openAppointmentDialog(self):
        try:
            # Create and show the AppointmentDialog
            appointment_dialog = AppointmentDialog(self)
            appointment_dialog.exec()  # Use exec() to show the dialog
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            print(f"Error opening appointment dialog: {e}")


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        # update_service_names()
        # delete_all_users()
        # delete_all_data()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)
