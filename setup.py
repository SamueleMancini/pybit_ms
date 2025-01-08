from setuptools import setup, find_packages

setup(
    name="pybit_ms",  # Package name on PyPI (must be unique)
    version="0.1.0",  # Start with 0.1.0, increment with changes
    author="Michelangelo Nardi and Samuele Mancini",
    author_email="nardimichelangelo@gmail.com, samuelemancini96@gmail.com",
    description="A modification of pybit library to facilitate trading automation and analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # README format
    url="https://github.com/SamueleMancini/pybit_ms",  # GitHub repo URL
    packages=find_packages(),  # Automatically find subpackages in `pybit_ms/`
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
    install_requires=[
    "requests",
    "crypto",
    "matplotlib",
    "pandas",
    "ipython"
    ],
)
