from setuptools import find_packages, setup

# Read the contents of the requirements file
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Kødudsalg",
    version="0.1.0",
    author="Søren Langkidle",
    author_email="soeren@langkilde.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        *requirements,
    ],
)
