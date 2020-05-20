from distutils.core import setup

setup(
    name='semester-progression',
    version='1.0',
    packages=['progression'],
    url='https://github.com/azharichenko/semester-progression',
    license='MIT License',
    author='Alex Zharichenko',
    author_email='azharichenko@gmail.com',
    description='',
    entry_points={
        "console_scripts": [
            "sp=progression.api:start_service_loop"
        ]
    }
)
