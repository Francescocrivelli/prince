from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip()
                    and not line.startswith("#")]

setup(
    name="prince",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
)
