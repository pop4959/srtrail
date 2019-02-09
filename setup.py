import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="srtrail",
    version="0.0.1",
    author="pop4959",
    author_email="pop4959@gmail.com",
    description="SpeedRunners trail editing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pop4959/srtrail",
    packages=setuptools.find_packages()
)
