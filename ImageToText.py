import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QGridLayout,
)

from PyQt5.QtCore import Qt, QTimer

from Capturer import Capture

class ScreenRegionSelector(QMainWindow):
    
    def __init__(self):
        super().__init__(None)
        self.m_width = 400
        self.m_height = 500

        self.setWindowTitle("Screen Capturer")
        self.setMinimumSize(self.m_width, self.m_height)

        frame = QFrame()
        frame.setContentsMargins(0, 0, 0, 0)
        self.layout = QGridLayout(frame)
        #lay = QVBoxLayout(frame)
        #lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #lay.setContentsMargins(5, 5, 5, 5)

        self.label = QLabel()
        self.btn_capture = QPushButton("Capture")
        self.btn_capture.clicked.connect(self.capture)
        
        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save)
        self.btn_save.setVisible(False)

        self.textbox = QTextEdit()
        self.textbox.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.btn_config_1 = QPushButton("--psm 6")
        self.btn_config_1.clicked.connect(lambda: self.set_config("--psm 6"))
        self.btn_config_2 = QPushButton("--psm 3")
        self.btn_config_2.clicked.connect(lambda: self.set_config("--psm 3"))
        self.btn_config_3 = QPushButton("--psm 5")
        self.btn_config_3.clicked.connect(lambda: self.set_config("--psm 5"))
        self.btn_config_4 = QPushButton("--psm 8")
        self.btn_config_4.clicked.connect(lambda: self.set_config("--psm 8"))
        self.btn_config_5 = QPushButton("--psm 13")
        self.btn_config_5.clicked.connect(lambda: self.set_config("--psm 13"))

        self.btn_config_1.setObjectName("ConfigButton")
        self.btn_config_1.setBaseSize(0, 0)

        self.layout.addWidget(self.btn_save, 0, 5, 1, 5)
        self.layout.addWidget(self.btn_capture, 0, 0, 1, 5)
        self.layout.addWidget(self.label, 1, 0, 4, 9)
        self.layout.addWidget(self.textbox, 5, 0, 5, 7)
        self.layout.addWidget(self.btn_config_1, 5, 7, 1, 3)
        self.layout.addWidget(self.btn_config_2, 6, 7, 1, 3)
        self.layout.addWidget(self.btn_config_3, 7, 7, 1, 3)
        self.layout.addWidget(self.btn_config_4, 8, 7, 1, 3)
        self.layout.addWidget(self.btn_config_5, 9, 7, 1, 3)

        self.setCentralWidget(frame)

    def set_config(self, config: str) -> None:
        extracted_text = self.capturer.extract_text(config)

    def capture(self) -> None:
        self.capturer = Capture(self)
        self.capturer.show()
        self.btn_save.setVisible(True)

    def save(self) -> None:
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image files (*.png *.jpg *.bmp)")
        if file_name:
            self.capturer.imgmap.save(file_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)    
    app.setStyleSheet("""
    QFrame {
        background-color: #3f3f3f;
    }
                      
    QPushButton {
        border-radius: 5px;
        background-color: rgb(60, 90, 255);
        padding: 10px;
        color: white;
        font-weight: bold;
        font-family: Arial;
        font-size: 12px;
    }
                      
    QPushButton::hover {
        background-color: rgb(60, 20, 255)
    }
                      
    QPushButton#ConfigButton {
        width: 50%;
    }
                      
    QTextEdit {
        color: rgb(255,255,255);
    }
    """)
    selector = ScreenRegionSelector()
    selector.show()
    app.exit(app.exec_())