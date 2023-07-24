from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="guards",
    version="0.0.2",
    author="Alias Innovations",
    author_email="",
    description="A package to ensure restrictions in form of guards in an application",
    keywords="guards",
    url="https://github.com/Alias-Innovations/python-guards",
    packages=find_packages(exclude=["tests", "examples"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    tests_require=["pytest"],
)
