import sys
from PyQt6.QtWidgets import QApplication
from mp3 import MP3

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mp3 = MP3()
    mp3.show()
    sys.exit(app.exec())