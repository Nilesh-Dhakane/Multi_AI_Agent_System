from setuptools import setup, find_packages

with open("requirements.txt") as file:
    requirements = file.read().splitlines()


setup(
    name="Multi-AI-Agent-System",
    author="Nilesh Dhakane",
    version="0.1",
    packages=find_packages(),
    install_requires = requirements,
    python_requires = ">=3.7"
)