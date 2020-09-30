import os
import runpy
import setuptools

HERE = os.path.dirname(__file__)
VERSION_FILE = os.path.join(HERE, "packaway", "version.py")
VERSION = runpy.run_path(VERSION_FILE)["__version__"]

setuptools.setup(
    name="packaway",
    license="MIT",
    version=VERSION,
    description="Check imports for enforcing encapsulation.",
    packages=setuptools.find_packages(),
    entry_points={
        "flake8.extension": [
            'DEP = packaway.plugins.flake8.import_checker:ImportChecker',
        ],
    },
)
