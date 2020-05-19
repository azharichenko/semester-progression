from datetime import date
from typing import NamedTuple

# from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont
from font_hanken_grotesk import HankenGroteskMedium
from progression.api import get_configuration_file


class InkyPHAT:
    WIDTH = 212
    HEIGHT = 104
    BLACK = 0
    WHITE = 255
    RED = 127


def draw_square(
        canvas: Image,
        x1=0,
        y1=0,
        x2=InkyPHAT.WIDTH,
        y2=InkyPHAT.HEIGHT,
        color=InkyPHAT.BLACK,
):
    for y in range(y1, y2):
        for x in range(x1, x2):
            canvas.putpixel((x, y), color)


def draw_dithered_square(
        canvas: Image,
        dither_amount=1,
        x1=0,
        y1=0,
        x2=InkyPHAT.WIDTH,
        y2=InkyPHAT.HEIGHT,
        color=InkyPHAT.BLACK,
):
    alternate = True
    for y in range(y1, y2):
        for x in range(x1, x2):
            if alternate:
                canvas.putpixel((x, y), color)
            else:
                canvas.putpixel((x, y), InkyPHAT.WHITE)
            alternate = not alternate
        alternate = not alternate


def draw_vertical_line(canvas: Image, v=0, y1=0, y2=InkyPHAT.HEIGHT, color=InkyPHAT.RED) -> None:
    for y in range(y1, y2):
        canvas.putpixel((v, y), color)


def draw_horizontal_line(canvas: Image, h=0, x1=0, x2=InkyPHAT.WIDTH, color=InkyPHAT.RED) -> None:
    for x in range(x1, x2):
        canvas.putpixel((x, h), color)


def determine_time_length(start: date, end: date, scaling: float = None) -> int:
    if scaling is not None:
        return int((end - start).days * scaling)
    return (end - start).days


def calculate_times(config, *, key=None, struct=None, scaling_factor=1):
    if key:
        return (
            determine_time_length(
                config["start"], config[key]["start"], scaling_factor
            ),
            determine_time_length(config["start"], config[key]["end"], scaling_factor),
        )
    if struct:
        return (
            determine_time_length(config["start"], struct["start"], scaling_factor),
            determine_time_length(config["start"], struct["end"], scaling_factor),
        )
    raise ValueError("key or struct is required")


def create_new_image() -> Image:
    return Image.new("L", size=(InkyPHAT.WIDTH, InkyPHAT.HEIGHT))


def draw_progress_bar(
        img: Image,
        percent: float = 0.25,
        x1: int = 0,
        y1: int = 0,
        x2: int = InkyPHAT.WIDTH,
        y2: int = InkyPHAT.HEIGHT,
        color=InkyPHAT.BLACK) -> Image:
    progress = x1 + int((x2 - x1) * percent)
    draw_square(img, x1=x1, y1=y1, x2=progress, y2=y2, color=color)


def draw_text(img: Image, text: str, color=InkyPHAT.BLACK):
    draw = ImageDraw.Draw(img)
    hanked_medium = ImageFont.truetype(HankenGroteskMedium, 20)

    text_w, text_h = hanked_medium.getsize(text)
    text_x = (InkyPHAT.WIDTH - text_w) // 2
    text_y = (InkyPHAT.HEIGHT - text_h) // 2
    draw.text((164, InkyPHAT.HEIGHT // 4 + 2), text, color, font=hanked_medium)


def draw_semester_display( y1=InkyPHAT.HEIGHT // 2, y2=InkyPHAT.HEIGHT) -> Image:
    today = date.today()
    config = get_configuration_file()

    time_length = determine_time_length(config["start"], config["end"])
    scaling_factor = InkyPHAT.WIDTH / time_length

    completed_duration = determine_time_length(config["start"], today, scaling_factor)

    midterm_start, midterm_end = calculate_times(
        config, key="midterm", scaling_factor=scaling_factor
    )
    finals_start, finals_end = calculate_times(
        config, key="finals", scaling_factor=scaling_factor
    )

    img = create_new_image()
    p = completed_duration / 212
    if p > 1:
        p = 1

    draw_square(img, color=InkyPHAT.WHITE)

    draw_progress_bar(img, percent=p, y1=InkyPHAT.HEIGHT // 2, y2=y2)

    draw_horizontal_line(img, h=InkyPHAT.HEIGHT // 2)
    draw_horizontal_line(img, h=InkyPHAT.HEIGHT // 4)
    draw_vertical_line(img, v=160, y2=InkyPHAT.HEIGHT // 2)
    draw_text(img, "Wow")

    draw_dithered_square(img, x1=midterm_start, x2=midterm_end, y1=y1, color=InkyPHAT.BLACK)
    draw_dithered_square(img, x1=finals_start, x2=finals_end, y1=y1, color=InkyPHAT.RED)

    for struct in config["breaks"]:
        start, end = calculate_times(
            config, struct=struct, scaling_factor=scaling_factor
        )
        start = determine_time_length(config["start"], struct["start"], scaling_factor)
        end = determine_time_length(config["start"], struct["end"], scaling_factor)
        draw_square(img, x1=start, x2=end, y1=y1, color=InkyPHAT.RED)

    for i in range(time_length // 7 + 1):
        draw_vertical_line(img, v=int(scaling_factor * i * 7), y1=y1)

    return img


#
# def _draw_to_display(img: Image) -> None:
#     # Set up properties of eInk display
#     inky_display = InkyPHAT("red")
#     inky_display.set_border(inky_display.BLACK)
#
#     # Display generated semester progress image
#     inky_display.set_image(img)
#     inky_display.show()


# def draw_display_message(text: str):
#     # Set up properties of eInk display
#     inky_display = InkyPHAT("red")
#     inky_display.set_border(inky_display.BLACK)
#
#     hanked_medium = ImageFont.truetype(HankenGroteskMedium, 20)
#
#     img = Image.new("P", size=(InkyPHAT.WIDTH, InkyPHAT.HEIGHT))
#     draw = ImageDraw.Draw(img)
#
#     text_w, text_h = hanked_medium.getsize(text)
#     text_x = (InkyPHAT.WIDTH - text_w) // 2
#     text_y = (InkyPHAT.HEIGHT - text_h) // 2
#     draw.text((text_x, text_y), text, InkyPHAT.BLACK, font=hanked_medium)
#
#     inky_display.set_image(img)
#     inky_display.show()
#

# def draw_to_display():
#     # Set up properties of eInk display
#     inky_display = InkyPHAT("red")
#     inky_display.set_border(inky_display.BLACK)
#
#     # Load previously generated image
#     img = create_new_image()
#
#     # Display generated semester progress image
#     inky_display.set_image(img)
#     inky_display.show()

if __name__ == "__main__":
    img = draw_semester_display()
    img.save("test.bmp")
