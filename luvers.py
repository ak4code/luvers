from PIL import Image, ImageDraw
import sys

ONE_INCH_IN_MM = 25.4

img = Image.open('print3.tif')

DPI = img.info['dpi'][0]

print(DPI)

step_in_mm = 200
offset_mm = 20
luvers_diametr = 10

width = img.width
height = img.height


def convert_to_mm(val):
    return val * 25.4


def convert_to_inch(val):
    return 25.4 / val


def convert_px_to_mm(val):
    return val * convert_to_inch(DPI)


def convert_mm_to_px(val):
    return round(val / convert_to_inch(DPI))


def get_one_pixel():
    return ONE_INCH_IN_MM / DPI


one_px = get_one_pixel()
step_in_px = convert_mm_to_px(step_in_mm)
offset_px = convert_mm_to_px(offset_mm)
luvers_diametr_px = convert_mm_to_px(luvers_diametr)

width_with_offset = width - (offset_px * 2)
height_with_offset = height - (offset_px * 2)

luvers_qnt_w = round(width / step_in_px)
luvers_qnt_h = round(height / step_in_px)
luvers_w_step = width_with_offset / luvers_qnt_w - 1
luvers_h_step = height_with_offset / luvers_qnt_h - 1

draw = ImageDraw.Draw(img)

print(width_with_offset)
print(height_with_offset)

step_w = round(luvers_w_step - round(luvers_diametr_px / (luvers_qnt_w - 1)))
step_h = round(luvers_h_step - round(luvers_diametr_px / (luvers_qnt_h - 1)))


def drawCircleWidth(x, y, step, luvers_d, luvers_qnt):
    for i in range(luvers_qnt):
        draw.ellipse([x, y, x + luvers_d, y + luvers_d], fill='black')
        x += step


def drawCircleHeight(x, y, step, luvers_d, luvers_qnt):
    for i in range(luvers_qnt):
        print(convert_px_to_mm(y))
        draw.ellipse([x, y, x + luvers_d, y + luvers_d], fill='black')
        y += step


x = offset_px
y = offset_px

drawCircleWidth(x, y, step_w, luvers_diametr_px, luvers_qnt_w)
drawCircleWidth(x + step_w, height - (offset_px + luvers_diametr_px), step_w, luvers_diametr_px, luvers_qnt_w)

drawCircleHeight(x, y + step_h, step_h, luvers_diametr_px, luvers_qnt_h)
drawCircleHeight(width - (offset_px + luvers_diametr_px), y, step_h, luvers_diametr_px, luvers_qnt_h)

img.save('print2.tif')
# img.show()
