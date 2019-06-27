from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PIL import Image, ImageDraw

import luvers


class LuversApp(QtWidgets.QMainWindow, luvers.Ui_MainWindow):
    im = None
    step = 300
    offset = 20
    luvers_size = 10
    top_side = True
    bottom_side = True
    left_side = True
    right_side = True
    only_corner = False
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
        self.btnOpenFile.clicked.connect(self.show_open_file_dialog)
        self.btnSaveFile.clicked.connect(self.show_save_file_dialog)
        self.stepInput.setText(str(self.step))
        self.cornerCheck.stateChanged.connect(self.set_only_corner)
        self.topAllCheck.stateChanged.connect(self.set_top_side)
        self.bottomAllCheck.stateChanged.connect(self.set_bottom_side)
        self.leftAllCheck.stateChanged.connect(self.set_left_side)
        self.rightAllCheck.stateChanged.connect(self.set_right_side)
        self.stepInput.textChanged.connect(self.set_step)

    def show_open_file_dialog(self):
        input_file = QFileDialog.getOpenFileName(self, 'Открыть файл', '.', 'TIFF(*.tif)')[0]

        self.im = Image.open(input_file, 'r')
        self.init_image()

    def show_save_file_dialog(self):
        if not self.im:
            return
        self.draw_luvers()
        # self.im.show()
        output_file = QFileDialog.getSaveFileName(self, 'Сохранить файл', '.', 'TIFF(*.tif)')[0]
        self.im.copy().save(output_file, compression='tiff_lzw')
        self.statusbar.showMessage('Файл сохранен!')

    def init_image(self):
        self.width_in_px = self.im.width
        self.height_in_px = self.im.height
        self.dpi = self.im.info['dpi'][0]
        self.set_pixel_size()

    def set_step(self):
        sender = self.sender()
        self.step = int(sender.text())

    def set_offset(self):
        sender = self.sender()
        self.step = int(sender.text())

    def set_only_corner(self):
        sender = self.sender()
        self.only_corner = sender.isChecked()
        self.topAllCheck.setChecked(False)
        self.bottomAllCheck.setChecked(False)
        self.leftAllCheck.setChecked(False)
        self.rightAllCheck.setChecked(False)

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

        if self.only_corner:
            left_corner_t = (offset_px, offset_px)
            left_corner_b = (offset_px, self.height_in_px - offset_px - luvers_size_px)
            right_corner_t = (self.width_in_px - offset_px - luvers_size_px, offset_px)
            right_corner_b = (
                self.width_in_px - offset_px - luvers_size_px, self.height_in_px - offset_px - luvers_size_px)
            self.make_luvers_only_corner(luvers_size_px, left_corner_t, left_corner_b, right_corner_t, right_corner_b)
            return True

        if self.top_side:
            luvers_qnt = round(self.width_in_px / step_px) + 1
            left_corner = (offset_px, offset_px)
            right_corner = (self.width_in_px - offset_px - luvers_size_px, offset_px)
            self.make_luvers_w(qnt=luvers_qnt, size=luvers_size_px, offset=offset_px, left=left_corner,
                               right=right_corner)

        if self.bottom_side:
            luvers_qnt = round(self.width_in_px / step_px) + 1
            left_corner = (offset_px, self.height_in_px - offset_px - luvers_size_px)
            right_corner = (
                self.width_in_px - offset_px - luvers_size_px, self.height_in_px - offset_px - luvers_size_px)
            self.make_luvers_w(qnt=luvers_qnt, size=luvers_size_px, offset=offset_px, left=left_corner,
                               right=right_corner)

        if self.right_side:
            luvers_qnt = round(self.height_in_px / step_px) + 1
            left_corner = (self.width_in_px - offset_px - luvers_size_px, offset_px)
            right_corner = (
                self.width_in_px - offset_px - luvers_size_px, self.height_in_px - offset_px - luvers_size_px)
            self.make_luvers_h(qnt=luvers_qnt, size=luvers_size_px, offset=offset_px, left=left_corner,
                               right=right_corner)

        if self.left_side:
            luvers_qnt = round(self.height_in_px / step_px) + 1
            left_corner = (offset_px, offset_px)
            right_corner = (offset_px, self.height_in_px - offset_px - luvers_size_px)
            self.make_luvers_h(qnt=luvers_qnt, size=luvers_size_px, offset=offset_px, left=left_corner,
                               right=right_corner)

    def make_luvers_only_corner(self, size, lt, lb, rt, rb):
        self.get_draw().ellipse([lt, (lt[0] + size, lt[1] + size)], fill='black')
        self.get_draw().ellipse([lb, (lb[0] + size, lb[1] + size)], fill='black')
        self.get_draw().ellipse([rt, (rt[0] + size, rt[1] + size)], fill='black')
        self.get_draw().ellipse([rb, (rb[0] + size, rb[1] + size)], fill='black')

    def make_luvers_w(self, qnt, size, offset, left, right):
        self.get_draw().ellipse([left, (left[0] + size, left[1] + size)], fill='black')
        self.get_draw().ellipse([right, (right[0] + size, right[1] + size)], fill='black')
        equal_step = ((self.width_in_px - offset * 2) / (qnt - 1)) - round(size / (qnt - 1))
        if qnt > 2:
            x1 = left[0] + equal_step
            for l in range(qnt - 2):
                self.get_draw().ellipse([(x1, left[1]), (x1 + size, left[1] + size)], fill='black')
                x1 += equal_step

    def make_luvers_h(self, qnt, size, offset, left, right):
        self.get_draw().ellipse([left, (left[0] + size, left[1] + size)], fill='black')
        self.get_draw().ellipse([right, (right[0] + size, right[1] + size)], fill='black')
        equal_step = ((self.height_in_px - offset * 2) / (qnt - 1)) - round(size / (qnt - 1))
        if qnt > 2:
            y1 = left[1] + equal_step
            for l in range(qnt - 2):
                self.get_draw().ellipse([(left[0], y1), (left[0] + size, y1 + size)], fill='black')
                y1 += equal_step


def main():
    appctxt = ApplicationContext()
    window = LuversApp()
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
