from setuptools import setup, find_packages
setup(
    name="bioviewer",  # Package name
    version="0.1.0",    # Initial release version
    author="Moritz Alkofer",
    author_email="moritz.alkofer@protonmail.com",
    description="This library is designed to build visualization tools for biosignals such as EEG or ECG.",
    url="https://github.com/MoritzAlkofer/BIOViewer",
    packages=find_packages(),
)