import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="subconfig",
    version="0.0.1",
    author="Filip Skóraś",
    author_email="fskoras@gmail.com",
    description="Configuration management library with value substitution for Python",
    license="MIT",
    keywords="configuration configuration-management configuration-parser configuration-files substitution",
    url="https://github.com/fskoras/subconfig",
    packages=["subconfig"],
    long_description=read('README.md'),
    install_requires=["flatdict"]
)
