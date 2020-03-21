from PIL import Image
from inky import InkyPHAT
from progression import util

# Get the semester progression path

config_path = util.get_config_path()

# Set up properties of eInk display
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.BLACK)

# Load previously generated image
img = Image.open(config_path / "gen/img.png")

# Display generated semester progress image

inky_display.set_image(img)
inky_display.show()