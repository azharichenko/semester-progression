from inky import InkyPHAT
from .draw import create_new_image

inky_display = InkyPHAT('red')
img = create_new_image()
inky_display.set_border(InkyPHAT.BLACK)
inky_display.set_image(img)
inky_display.show()