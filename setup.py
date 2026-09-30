"""Setup configuration for VeriFactu Python package."""
from setuptools import setup, find_packages

version = '1.0.68'

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("LICENSE", encoding="utf-8") as f:
    license_text = f.read()

setup(
    name="VeriFactu",
    version=version,
    description="Generación, conservación y envío facturas VERI*FACTU de la AEAT",
    long_description="Generación, conservación y envío de facturas VERI*FACTU para la AEAT.",
    long_description_content_type="text/markdown",
    author="Diogo Gouveia",
    author_email="diogo.gouveia2@gmail.com",
    url="https://github.com/drjgouveia/VeriFactu",
    license="GNU AFFERO GENERAL PUBLIC LICENSE",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.14",
)