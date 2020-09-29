import setuptools

setuptools.setup(
    name="packaway",
    license="MIT",
    version="0.1.0",
    description="Check imports for enforcing encapsulation.",
    packages=setuptools.find_packages(
        where='packaway',
    ),
    entry_points={
        "flake8.extension": [
            'ARC = packaway.plugins.flake8.import_checker:ImportChecker',
        ],
    },
)
