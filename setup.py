from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='monkeyrider',
    version='0.0.1',
    url='https://github.com/bnznamco/monkeyrider',
    install_requires=[
        'xmltodict==0.11.0'
    ],
    entry_points={
        'console_scripts': ['monkeyrider=monkeyrider.monkeyrider:main'],
    },
    description="A tool to guide monkeys through unknown apks",
    long_description=long_description,
    license="MIT",
    author="Gabriele Baldi",
    author_email="gabriele.baldi.01@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Environment :: Android Environment',
        'Framework :: Monkeyrunner',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)
