from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bioviewer",  # Package name
    version="0.2.3",    # Initial release version
    author="Moritz Alkofer",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify Markdown (use 'text/x-rst' for reStructuredText)
    author_email="moritz.alkofer@protonmail.com",
    description="This library is designed to build visualization tools for biosignals such as EEG or ECG.",
    url="https://github.com/MoritzAlkofer/BIOViewer",
    packages=find_packages(),
)
