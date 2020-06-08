from setuptools import setup

setup(
    name='semester-progression',
    version='1.0',
    packages=['pidriver'],
    url='https://github.com/azharichenko/semester-progression',
    license='MIT License',
    author='Alex Zharichenko',
    author_email='azharichenko@gmail.com',
    description='',
    entry_points={
        "console_scripts": [
            "sp=pidriver.api:start"
        ]
    }
)
