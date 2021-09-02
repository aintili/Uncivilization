from setuptools import find_packages
from setuptools import setup

setup(
    name="Uncivilization",
    version="1.0.0",
    description="A 4x game with a familiar feel",
    author="Anthony Intili",
    packages=find_packages(),
    entry_points={"console_scripts": ["Unciv=Uncivilization.__main__:main"]},
    install_requires=["pygame", "numpy"],
)
