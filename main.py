import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PIL import Image, ImageDraw

import luvers_app


class LuversApp(QtWidgets.QMainWindow, luvers_app.Ui_MainWindow):
    im = None
    step = 100
    offset = 20
    luvers_size = 10
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
        self.topAllCheck.stateChanged.connect(self.set_top_side)
        self.bottomAllCheck.stateChanged.connect(self.set_bottom_side)
        self.leftAllCheck.stateChanged.connect(self.set_left_side)
        self.rightAllCheck.stateChanged.connect(self.set_right_side)
        self.stepInput.textChanged.connect(self.set_step)
        self.offsetInput.textChanged.connect(self.set_offset)

    def show_open_file_dialog(self):
        input_file = QFileDialog.getOpenFileName(self, 'Открыть файл', '.', 'TIFF(*.tif)')[0]

        self.im = Image.open(input_file, 'r')
        self.init_image()

    def show_save_file_dialog(self):
        if not self.im:
            return
        self.draw_luvers()
        self.im.show()
        # output_file = QFileDialog.getSaveFileName(self, 'Сохранить файл', '.', 'TIFF(*.tif)')[0]
        # self.im.copy().save(output_file, compression='tiff_lzw')

    def init_image(self):
        self.width_in_px = self.im.width
        self.height_in_px = self.im.height
        self.dpi = self.im.info['dpi'][0]
        self.set_pixel_size()
        self.banerWidth.setText(str(self.convert_px_to_mm(self.im.width)))
        self.banerHeight.setText(str(self.convert_px_to_mm(self.im.height)))

    def set_step(self):
        sender = self.sender()
        self.step = int(sender.text())

    def set_offset(self):
        sender = self.sender()
        self.step = int(sender.text())

    def set_top_side(self):
        sender = self.sender()
        self.top_side = sender.isChecked()

    def set_bottom_side(self):
        sender = self.sender()
        self.bottom_side = sender.isChecked()

    def set_left_side(self):
        sender = self.sender()
        self.left_side = sender.isChecked()

    def set_right_side(self):
        sender = self.sender()
        self.right_side = sender.isChecked()

    def set_pixel_size(self):
        self.pixel_size = self.inch_in_mm / self.dpi

    def convert_px_to_mm(self, val):
        return round(val * self.pixel_size)

    def convert_mm_to_px(self, val):
        return round(val / self.pixel_size)

    def get_draw(self):
        draw = ImageDraw.Draw(self.im)
        return draw

    def draw_luvers(self):
        if not self.im:
            return

        luvers_size_px = self.convert_mm_to_px(self.luvers_size)
        offset_px = self.convert_mm_to_px(self.offset)
        step_px = self.convert_mm_to_px(self.step)

        if self.top_side:
            luvers_qnt = round(self.width_in_px / step_px) + 1
            left_corner = (offset_px, offset_px)
            right_corner = (self.width_in_px - offset_px - luvers_size_px, offset_px)
            self.make_luvers(qnt=luvers_qnt, size=luvers_size_px, offset=offset_px, left=left_corner,
                             right=right_corner)

        if self.bottom_side:
            luvers_qnt = round(self.width_in_px / step_px) + 1
            left_corner = (offset_px, self.height_in_px - offset_px - luvers_size_px)
            right_corner = (
            self.width_in_px - offset_px - luvers_size_px, self.height_in_px - offset_px - luvers_size_px)
            self.make_luvers(qnt=luvers_qnt, size=luvers_size_px, offset=offset_px, left=left_corner,
                             right=right_corner)

    def make_luvers(self, qnt, size, offset, left, right):
        self.get_draw().ellipse([left, (left[0] + size, left[1] + size)], fill='black')
        self.get_draw().ellipse([right, (right[0] + size, right[1] + size)], fill='black')
        equal_step = ((self.width_in_px - offset * 2) / (qnt - 1)) - round(size / (qnt - 1))
        if qnt > 2:
            print(f'Расстояние между люверсами: {self.convert_px_to_mm(equal_step)}')
            x1 = left[0] + equal_step
            for l in range(qnt - 2):
                print(f'Точка по X: {self.convert_px_to_mm(x1)}')
                self.get_draw().ellipse([(x1, left[1]), (x1 + size, left[1] + size)], fill='black')
                x1 += equal_step


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LuversApp()
    window.show()
    exit_code = app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
