from PIL import Image, ImageDraw
from progression.util import InkyPHATProperties as InkyPHAT

canvas = Image.new("RGB", size=(InkyPHAT.HEIGHT, InkyPHAT.WIDTH))