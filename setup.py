from setuptools import find_packages, setup

setup(
    name="example",
    version="0.1.0",
    packages=find_packages(include=["dhp", "dhp.*"]),
    install_requires=[
        "alembic~=1.8",
        "flask~=2.1",
        "pandas~=1.4",
        "sqlalchemy~=1.4",
        "psycopg2-binary~=2.9",
        "matplotlib~=3.5"
    ],
    extras_require={
        "dev": ["pytest", "ipython"],
    },
)
