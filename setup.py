# Purpose : Package and distribution management.
# If your module package is at the root of your repository, this should obviously be at the root as well.

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="turkish_validator",  # This is the name of the package
    version="0.0.1",  # The initial release version
    author="Hasan Özdemir",  # Full name of the author
    author_email="hasann.ozdemirr58@gmail.com",  # Author contact
    description="Turkish ID number and Turkish Tax number validation",
    long_description=long_description,  # Long description read from the readme file
    long_description_content_type="text/markdown",
    packages=["turkish_validator"],  # Directory of the source code of the package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    keywords=[
        "data science",
        "python",
        "validation",
        "turkish_id",
        "tax_number",
        "web_development",
    ],
    python_requires=">=3.7",  # Minimum version requirement of the package
    install_requires=[],  # Install other dependencies if any
)
