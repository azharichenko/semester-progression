from datetime import date

from inky import InkyPHAT
from PIL import Image, ImageDraw
from progression.util import get_configuration_file


def create_new_image():
    today = date.today()
    configuration = get_configuration_file()

    time_length = (configuration['end-date'] - configuration['start-date']).days
    scaling_factor = InkyPHAT.WIDTH / time_length
    completed_duration = (today - configuration['start-date']).days
    completed_duration = int(completed_duration * scaling_factor)
    print(time_length, scaling_factor, completed_duration)
    canvas = Image.new("P", size=(InkyPHAT.WIDTH, InkyPHAT.HEIGHT))
    draw = ImageDraw.Draw(canvas)

    for y in range(0, InkyPHAT.HEIGHT):
        for x in range(0, completed_duration):
            canvas.putpixel((x, y), InkyPHAT.BLACK)

    return canvas


def draw_to_display():
    # Set up properties of eInk display
    inky_display = InkyPHAT("red")
    inky_display.set_border(inky_display.BLACK)

    # Load previously generated image
    img = draw.create_new_image()

    # Display generated semester progress image

    inky_display.set_image(img)
    inky_display.show()