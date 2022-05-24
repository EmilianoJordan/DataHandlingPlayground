from setuptools import find_packages, setup

setup(
    name="example",
    version="0.1.0",
    packages=find_packages(include=["dhp", "dhp.*"]),
    install_requires=["pandas>=1.4.2", "sqlalchemy>=1.4.36", "flask>=2.1.2"],
    extras_require={
        "dev": ["pytest"],
    },
)
