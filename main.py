import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PIL import Image

import luvers_app


class LuversApp(QtWidgets.QMainWindow, luvers_app.Ui_MainWindow):
    im = None
    step = 300
    offset = 200
    top_side = False
    bottom_side = False
    left_side = False
    right_side = False
    dpi = 0
    pixel_size = 0
    inch_in_mm = 25.4
    width_in_px = 0
    height_in_px = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Расчет люверсов')
        self.btnOpenFile.clicked.connect(self.show_open_file_dialog)
        self.btnSaveFile.clicked.connect(self.show_save_file_dialog)
        self.stepInput.setText(str(self.step))
        self.offsetInput.setText(str(self.offset))
        self.topAllCheck.setChecked(self.top_side)
        self.stepInput.textChanged.connect(self.set_step)
        self.offsetInput.textChanged.connect(self.set_offset)

    def show_open_file_dialog(self):
        input_file = QFileDialog.getOpenFileName(self, 'Открыть файл', '.')[0]

        self.im = Image.open(input_file, 'r')
        self.init_image()

    def show_save_file_dialog(self):
        output_file = QFileDialog.getSaveFileName(self, 'Сохранить файл', '.', 'TIFF(*.tif)')[0]
        self.im.save(output_file)

    def init_image(self):
        self.width_in_px = self.im.width
        self.height_in_px = self.im.height
        self.dpi = self.im.info['dpi'][0]
        self.set_pixel_size()
        self.banerWidth.setText(str(self.convert_px_to_mm(self.im.width)))
        self.banerHeight.setText(str(self.convert_px_to_mm(self.im.height)))

    def set_step(self):
        sender = self.sender()
        self.step = sender.text()

    def set_offset(self):
        sender = self.sender()
        self.step = sender.text()

    def set_pixel_size(self):
        self.pixel_size = self.inch_in_mm / self.dpi

    def convert_px_to_mm(self, val):
        return round(val * self.pixel_size)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LuversApp()
    window.show()
    exit_code = app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
