from setuptools import setup

setup(
    name="semester-progression",
    version="1.2",
    packages=["pidriver"],
    url="https://github.com/azharichenko/semester-progression",
    license="MIT License",
    author="Alex Zharichenko",
    author_email="azharichenko@gmail.com",
    description="",
    install_requires=["parse", "pillow", "requests", "ics",],
    entry_points={"console_scripts": ["sp=pidriver.api:start"]},
)
