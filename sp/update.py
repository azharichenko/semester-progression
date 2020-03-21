#!/usr/bin/python3

from pathlib import Path
from PIL import Image
from inky import InkyPHAT

# Get the semester progression path

config_path = Path("~") / '.sp_config'
if not config_path.exists():
    raise RuntimeError("Can't find ~/.sp_config directory")

# Set up properties of eInk display
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.BLACK)

# Load previously generated image
img = Image.open(config_path / "gen/img.png")

# Display generated semester progresss image

inky_display.set_image(img)
inky_display.show()