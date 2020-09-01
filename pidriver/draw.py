from datetime import date
from typing import Tuple, Generator

from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont
from font_hanken_grotesk import HankenGroteskMedium
from pidriver.data import get_semester_file, Period


# class InkyPHAT:
#     WIDTH: int = 212
#     HEIGHT: int = 104
#     BLACK: int = 0
#     WHITE: int = 255
#     RED: int = 127


HALF_H = InkyPHAT.HEIGHT // 2
QUARTER_H = InkyPHAT.HEIGHT // 4
DIVIDER = 160


def draw_square(
    canvas: Image,
    x1: int = 0,
    y1: int = 0,
    x2: int = InkyPHAT.WIDTH,
    y2: int = InkyPHAT.HEIGHT,
    color=InkyPHAT.BLACK,
) -> None:
    for y in range(y1, y2):
        for x in range(x1, x2):
            canvas.putpixel((x, y), color)


def draw_dithered_square(
    canvas: Image,
    x1: int = 0,
    y1: int = 0,
    x2: int = InkyPHAT.WIDTH,
    y2: int = InkyPHAT.HEIGHT,
    color=InkyPHAT.BLACK,
) -> None:
    alternate: bool = True
    for y in range(y1, y2):
        for x in range(x1, x2):
            if alternate:
                canvas.putpixel((x, y), color)
            else:
                canvas.putpixel((x, y), InkyPHAT.WHITE)
            alternate = not alternate
        alternate = not alternate


def draw_vertical_line(
    canvas: Image,
    v: int = 0,
    y1: int = 0,
    y2: int = InkyPHAT.HEIGHT,
    color=InkyPHAT.RED,
) -> None:
    for y in range(y1, y2):
        canvas.putpixel((v, y), color)


def draw_horizontal_line(
    canvas: Image, h: int = 0, x1: int = 0, x2: int = InkyPHAT.WIDTH, color=InkyPHAT.RED
) -> None:
    for x in range(x1, x2):
        canvas.putpixel((x, h), color)


def determine_time_length(start: date, end: date, scaling: float = None) -> int:
    if scaling is not None:
        return int((end - start).days * scaling)
    return (end - start).days


def calculate_period_delta(
    semester_period: Period, period: Period, scaling_factor: float = 1.0
) -> Tuple:
    return (
        determine_time_length(semester_period.start, period.start, scaling_factor),
        determine_time_length(semester_period.start, period.end, scaling_factor),
    )


def calculate_times(config, *, key=None, struct=None, scaling_factor: float = 1.0):
    if key:
        return (
            determine_time_length(
                config.period.start, config[key].start, scaling_factor
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
    return Image.new("P", size=(InkyPHAT.WIDTH, InkyPHAT.HEIGHT))


def draw_progress_bar(
    img: Image,
    percent: float = 0.25,
    x1: int = 0,
    y1: int = 0,
    x2: int = InkyPHAT.WIDTH,
    y2: int = InkyPHAT.HEIGHT,
    color=InkyPHAT.BLACK,
) -> Image:
    progress = x1 + int((x2 - x1) * percent)
    draw_square(img, x1=x1, y1=y1, x2=progress, y2=y2, color=color)


def draw_text(
    img: Image,
    text: str,
    x1: int = 0,
    y1: int = 0,
    x2: int = InkyPHAT.WIDTH,
    y2: int = InkyPHAT.HEIGHT,
    color=InkyPHAT.BLACK,
) -> None:
    assert x1 < x2
    assert x1 >= 0
    draw = ImageDraw.Draw(img)
    font = 20

    text_w = 0
    text_h = 0

    hanked_medium = ImageFont.truetype(HankenGroteskMedium, font)
    while font > 0:
        text_w, text_h = hanked_medium.getsize(text)
        if (x2 - x1 - text_w) > 0 and (y2 - y1 - text_h) > 0:
            break
        font -= 1
        hanked_medium = ImageFont.truetype(HankenGroteskMedium, font)
    if font == 0:
        raise ValueError("Text not able to be displayed")

    text_x = x1 + (x2 - x1 - text_w) // 2
    text_y = y1 + (y2 - y1 - text_h) // 2
    draw.text((text_x, text_y), text, color, font=hanked_medium)


def sunday_tick_marks(
    period: Period, scaling_factor: float
) -> Generator[int, None, None]:
    sunday_distance = 6 - period.start.isoweekday()
    total_length = (period.end - period.start).days
    days = sunday_distance

    while days < total_length:
        yield int(days * scaling_factor)
        days += 7


def draw_semester_display(y1: int = HALF_H, y2: int = InkyPHAT.HEIGHT) -> Image:
    today = date.today()
    config = get_semester_file()

    time_length = determine_time_length(config.period.start, config.period.end)
    scaling_factor = InkyPHAT.WIDTH / time_length
    completed_duration = determine_time_length(
        start=config.period.start, end=today, scaling=scaling_factor
    )

    midterm_start, midterm_end = calculate_period_delta(
        semester_period=config.period,
        period=config.midterms,
        scaling_factor=scaling_factor,
    )
    finals_start, finals_end = calculate_period_delta(
        semester_period=config.period,
        period=config.finals,
        scaling_factor=scaling_factor,
    )

    img = create_new_image()
    p = completed_duration / 212
    if p > 1:
        p = 1

    draw_square(img, color=InkyPHAT.WHITE)

    draw_progress_bar(img, percent=p, y1=HALF_H, y2=y2)

    draw_horizontal_line(img, h=HALF_H)
    draw_horizontal_line(img, h=QUARTER_H)
    draw_vertical_line(img, v=DIVIDER, y2=HALF_H)

    draw_text(
        img,
        str(time_length - (date.today() - config.period.start).days),
        x1=DIVIDER,
        y1=-4,
        y2=QUARTER_H,
    )
    draw_text(
        img, " {}% ".format(int(p * 100)), x1=DIVIDER, y1=QUARTER_H - 4, y2=HALF_H
    )

    top_text: str
    bottom_text: str
    if len(config.events) >= 2:
        first_event, second_event = config.events[0], config.events[1]
        top_text = "{} - {}/{}".format(
            first_event.name, first_event.date.month, first_event.date.day
        )
        bottom_text = "{} - {}/{}".format(
            second_event.name, second_event.date.month, second_event.date.day
        )
    elif len(config.events) >= 1:
        first_event = config.events[0]
        top_text = "{} - {}/{}".format(
            first_event.name, first_event.date.month, first_event.date.day
        )
        bottom_text = ""
    else:
        top_text = "No events"
        bottom_text = ""

    draw_text(img, top_text, x2=DIVIDER, y1=0, y2=QUARTER_H)
    draw_text(img, bottom_text, x2=DIVIDER, y1=QUARTER_H, y2=HALF_H)

    draw_dithered_square(
        img, x1=midterm_start, x2=midterm_end, y1=y1, color=InkyPHAT.BLACK
    )
    draw_dithered_square(img, x1=finals_start, x2=finals_end, y1=y1, color=InkyPHAT.RED)

    # TODO: Reimplement breaks
    # for struct in config["breaks"]:
    #     start, end = calculate_times(
    #         config, struct=struct, scaling_factor=scaling_factor
    #     )
    #     start = determine_time_length(config["start"], struct["start"], scaling_factor)
    #     end = determine_time_length(config["start"], struct["end"], scaling_factor)
    #     draw_square(img, x1=start, x2=end, y10=y1, color=InkyPHAT.RED)

    for sunday in sunday_tick_marks(config.period, scaling_factor=scaling_factor):
        draw_vertical_line(img, v=sunday, y1=y1)

    return img


#
def _draw_to_display(img: Image) -> None:
    # Set up properties of eInk display
    inky_display = InkyPHAT("red")
    inky_display.set_border(inky_display.BLACK)

    # Display generated semester progress image
    inky_display.set_image(img)
    inky_display.show()


def draw_display_message(text: str):
    # Set up properties of eInk display
    inky_display = InkyPHAT("red")
    inky_display.set_border(inky_display.BLACK)

    hanked_medium = ImageFont.truetype(HankenGroteskMedium, 20)

    img = Image.new("P", size=(InkyPHAT.WIDTH, InkyPHAT.HEIGHT))
    draw = ImageDraw.Draw(img)

    text_w, text_h = hanked_medium.getsize(text)
    text_x = (InkyPHAT.WIDTH - text_w) // 2
    text_y = (InkyPHAT.HEIGHT - text_h) // 2
    draw.text((text_x, text_y), text, InkyPHAT.BLACK, font=hanked_medium)

    inky_display.set_image(img)
    inky_display.show()


def draw_to_display():
    # Set up properties of eInk display
    inky_display = InkyPHAT("red")
    inky_display.set_border(inky_display.BLACK)

    # Load previously generated image
    img = draw_semester_display()

    # Display generated semester progress image
    inky_display.set_image(img)
    inky_display.show()


# def draw_to_display():
#     img = draw_semester_display()
#     img.save("test.bmp")
