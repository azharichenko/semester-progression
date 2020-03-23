from datetime import date

from inky import InkyPHAT
from PIL import Image, ImageDraw
from progression.util import get_configuration_file


def draw_square(canvas, x1=0, y1=0, x2=InkyPHAT.WIDTH, y2=InkyPHAT.HEIGHT, color=InkyPHAT.BLACK):
    for y in range(y1, y2):
        for x in range(x1, x2):
            canvas.putpixel((x, y), color)


def draw_dithered_square(canvas, dither_amount=1, x1=0, y1=0, x2=InkyPHAT.WIDTH, y2=InkyPHAT.HEIGHT,
                         color=InkyPHAT.BLACK):
    for y in range(y1, y2):
        for x in range(x1, x2, 1 + dither_amount):
            canvas.putpixel((x + (y % (1 + dither_amount)), y), color)


def draw_line(canvas, h=None, v=None):
    for y in range(0, InkyPHAT.HEIGHT):
        canvas.putpixel((v, y), InkyPHAT.RED)


def determine_time_length(start, end, scaling=None):
    if scaling is not None:
        return int((end - start).days * scaling)
    return (end - start).days


def create_new_image():
    today = date.today()
    configuration = get_configuration_file()

    time_length = determine_time_length(configuration['start-date'], configuration['end-date'])
    scaling_factor = InkyPHAT.WIDTH / time_length

    completed_duration = determine_time_length(configuration['start-date'], today, scaling_factor)

    finals_start = determine_time_length(configuration['start-date'], configuration['finals']['start-date'],
                                         scaling_factor)
    finals_end = determine_time_length(configuration['start-date'], configuration['finals']['end-date'], scaling_factor)

    img = Image.new("P", size=(InkyPHAT.WIDTH, InkyPHAT.HEIGHT))
    ImageDraw.Draw(img)

    draw_square(img, x2=completed_duration)
    draw_dithered_square(img, x1=finals_start, x2=finals_end, color=InkyPHAT.RED)

    for i in range(time_length // 7 + 1):
        draw_line(img, v=int(scaling_factor * i * 7))

    return img


def draw_to_display():
    # Set up properties of eInk display
    inky_display = InkyPHAT("red")
    inky_display.set_border(inky_display.BLACK)

    # Load previously generated image
    img = create_new_image()

    # Display generated semester progress image

    inky_display.set_image(img)
    inky_display.show()
