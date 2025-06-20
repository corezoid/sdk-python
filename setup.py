from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="corezoid-sdk",
    version="0.1.0",
    author="Corezoid",
    author_email="support@corezoid.com",
    description="Python SDK for Corezoid Process Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/corezoid/sdk-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "pycryptodome>=3.10.1",
    ],
)
