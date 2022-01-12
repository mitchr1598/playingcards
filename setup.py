import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="playingcards1598",
    version="1.1.3",
    description="An Advanced and Customisable Python Playing Card Module that makes creating playing card games and running simulations general, simple and easy!",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mitchr1598/playingcards",
    author="mitchr1598",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    packages=["playingcards"],
    python_requires=">=3.9.0",
)
