import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="physics-error-calculator",
    version="0.1",
    author="Tobias Juelg",
    author_email="",
    description="Automatically error calculation as used in physics with the output of the latex code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JobiProGrammer/error-calculator",
    packages=setuptools.find_packages(),
    install_requires=['sympy', 'numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)