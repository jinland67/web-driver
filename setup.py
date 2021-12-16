from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='web-driver',
    version='0.1.0',
    author='jinland',
    author_email='jinland@bommaru.com',
    description='Library for using selenium web driver',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/bommaru-com/web_driver.git',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: Selenium Approved :: Bommaru License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.10',
    install_requires=[
        'beautifulsoup4 >= 4.10.0',
        'selenium >= 4.0.0',
    ],
    package_data={"web_driver": ["*.txt"]},
    include_package_data=True,
)