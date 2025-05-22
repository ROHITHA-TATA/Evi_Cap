import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Debug Test")
    window.setGeometry(100, 100, 300, 200)
    
    button = QPushButton("Test Button", window)
    button.move(100, 80)
    button.clicked.connect(lambda: print("Button clicked!"))
    
    window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
