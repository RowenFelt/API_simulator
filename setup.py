import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="httpantry",
    version="0.0.1",
    author="Rowen Felt, Zebediah Millslagle",
    author_email="rfelt@middlebury.edu, zmillslagle@gmail.com",
    description="Stores and returns HTTP requests for faster, more efficient development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RowneFelt/httproxy",
    packages=['httpantry'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts" : [
            "httpantry = httpantry.command_line:main",
        ]
    }
)