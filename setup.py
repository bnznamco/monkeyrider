import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="monkeyrider",
    version="0.0.1",
    author="bnznamco",
    author_email="gabriele.baldi.01@gmail.com",
    description="A tool to guide monkeys through unknown apks",
    url="https://github.com/bnznamco/monkeyrider",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
