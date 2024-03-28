#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


from setuptools import find_packages, setup

MAIN_REQUIREMENTS = ["airbyte-cdk", "firebolt-sdk>=0.14.0"]

TEST_REQUIREMENTS = [
    "requests-mock",
    "pytest-mock",
    "pytest>=6.2.5",  # 6.2.5 has python10 compatibility fixes
    "pytest-asyncio>=0.18.0",
]

setup(
    entry_points={
        "console_scripts": [
            "source-firebolt=source_firebolt.run:run",
        ],
    },
    name="source_firebolt",
    description="Source implementation for Firebolt.",
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
