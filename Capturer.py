from PyQt5.QtWidgets import QWidget, QApplication, QRubberBand
from PyQt5.QtGui import QMouseEvent, QClipboard
from PyQt5.QtCore import Qt, QPoint, QRect
import time
from OCR import ImageReader, OS

class Capture(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.image_reader = ImageReader(OS.Windows)
        self.main = main_window
        self.main.hide()
        
        self.setMouseTracking(True)
        desk_size = QApplication.desktop()
        self.setGeometry(0, 0, desk_size.width(), desk_size.height())
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.5)

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()


        QApplication.setOverrideCursor(Qt.CrossCursor)
        screen = QApplication.primaryScreen()
        rect = QApplication.desktop().rect()

        time.sleep(0.31)
        self.imgmap = screen.grabWindow(
            QApplication.desktop().winId(),
            rect.x(), rect.y(), rect.width(), rect.height()
        )

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rubber_band.show() 

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        if not self.origin.isNull():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def extract_text(self, config:str="--psm 6") -> str:
        if (config):
            self.image_reader.config = config
        extracted_text = self.image_reader.extract_text()
        self.main.textbox.setText(extracted_text)
        return extracted_text

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.rubber_band.hide()
            
            rect = self.rubber_band.geometry()
            self.imgmap = self.imgmap.copy(rect)
            QApplication.restoreOverrideCursor()

            # set clipboard
            clipboard = QApplication.clipboard()

            self.imgmap.save("TEST.png")
            extracted_text = self.extract_text()
            clipboard.setText(extracted_text)
#            print(extracted_text)
            self.main.label.setPixmap(self.imgmap)
            self.main.show()

            

            self.close()