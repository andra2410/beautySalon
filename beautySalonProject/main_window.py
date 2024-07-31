import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QDialog
from PyQt6.QtGui import QPixmap
from PyQt6 import QtCore
from PyQt6.uic import loadUi
from meet_the_team import MeetTheTeam  # Import the new window class

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main_window.ui", self)

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
        print("Book appointment")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())