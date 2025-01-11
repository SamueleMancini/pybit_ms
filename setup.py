from setuptools import setup, find_packages

setup(
    name="pybit_ms",
    version="0.1.8",
    author="Michelangelo Nardi and Samuele Mancini",
    author_email="nardimichelangelo@gmail.com, samuelemancini96@gmail.com",
    description="A modification of pybit library to facilitate trading automation and analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SamueleMancini/pybit_ms",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        "requests",
        "pycryptodome",
        "matplotlib",
        "pandas",
        "ipython",
    ],
    license="MIT", 
)
