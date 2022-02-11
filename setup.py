import setuptools

with open("README.md", "r") as f:
	desc = f.read()

import re

with open("nsgi/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

setuptools.setup(
    name="nsgi",
    version=version,
    author="Alex Hutz",
	long_description=desc,
    author_email="frostiitheweeb@outlook.com",
    description="A wrapper for Redis.",
    url="https://github.com/OpenRobot-Packages/nsgi",
    project_urls={
        "Bug Tracker": "https://github.com/OpenRobot-Packages/nsgi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
    ],
    packages=["nsgi", "nsgi.plugins"],
    python_requires=">=3.7",
)