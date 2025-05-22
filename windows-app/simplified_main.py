import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QComboBox, QLabel, QLineEdit, QMessageBox,
                             QGroupBox, QHBoxLayout, QRadioButton)
from PyQt5.QtCore import Qt

class SimplifiedTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simplified Tool")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Platform Selection Group
        platform_group = QGroupBox("Platform Selection")
        platform_layout = QVBoxLayout()
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["Reddit", "Mastodon"])
        platform_layout.addWidget(QLabel("Select Platform:"))
        platform_layout.addWidget(self.platform_combo)
        platform_group.setLayout(platform_layout)
        main_layout.addWidget(platform_group)
        
        # Input Group
        input_group = QGroupBox("Account Information")
        input_layout = QVBoxLayout()
        self.profile_id_label = QLabel("Profile ID/Username:")
        self.profile_id_input = QLineEdit()
        input_layout.addWidget(self.profile_id_label)
        input_layout.addWidget(self.profile_id_input)
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.extract_button = QPushButton("Extract Data")
        self.extract_button.clicked.connect(self.extract_data)
        button_layout.addWidget(self.extract_button)
        main_layout.addLayout(button_layout)
        
    def extract_data(self):
        platform = self.platform_combo.currentText()
        profile_id = self.profile_id_input.text()
        QMessageBox.information(self, "Success", f"Selected platform: {platform}\nProfile ID: {profile_id}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimplifiedTool()
    window.show()
    try:
        sys.exit(app.exec())
    except AttributeError:
        sys.exit(app.exec_())
