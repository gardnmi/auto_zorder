from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "SIMPLEREADME.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.3"
DESCRIPTION = "The project aims to remove the guesswork of selecting columns to be used in the ZORDER statement. It achieves this by analyzing the logged execution plan for each cluster provided and returns the top n columns that were used in filter/where clauses."

# Setting up
setup(
    name="auto_zorder",
    version=VERSION,
    author="Michael Gardner",
    author_email="gardnmi@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[""],
    keywords=["python", "databricks", "delta", "spark"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
