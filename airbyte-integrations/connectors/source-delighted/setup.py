#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


from setuptools import find_packages, setup

MAIN_REQUIREMENTS = [
    "airbyte-cdk",
]

TEST_REQUIREMENTS = [
    "requests-mock",
    "pytest-mock",
    "pytest",
    "responses~=0.13.3",
]

setup(
    entry_points={
        "console_scripts": [
            "source-delighted=source_delighted.run:run",
        ],
    },
    name="source_delighted",
    description="Source implementation for Delighted.",
    author="Airbyte",
    author_email="contact@airbyte.io",
    packages=find_packages(),
    install_requires=MAIN_REQUIREMENTS,
    package_data={
        "": [
            # Include yaml files in the package (if any)
            "*.yml",
            "*.yaml",
            # Include all json files in the package, up to 4 levels deep
            "*.json",
            "*/*.json",
            "*/*/*.json",
            "*/*/*/*.json",
            "*/*/*/*/*.json",
        ]
    },
    extras_require={
        "tests": TEST_REQUIREMENTS,
    },
)
