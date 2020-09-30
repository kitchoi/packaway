import os
import runpy
import setuptools

HERE = os.path.dirname(__file__)
VERSION_FILE = os.path.join(HERE, "packaway", "version.py")
VERSION = runpy.run_path(VERSION_FILE)["__version__"]

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="packaway",
    license="MIT",
    version=VERSION,
    description="Static Checker to Enforce (Some) Encapsulation in Python.",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/kitchoi/packaway",
    entry_points={
        "flake8.extension": [
            'DEP = packaway.plugins.flake8.import_checker:ImportChecker',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
