import setuptools

long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Pingme!",
    version="0.0.1",
    author="Steve Nalos",
    author_email="steveanthony.nalos@gmail.com",
    description="A lambda function used for logging and notification system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: Other/Proprietary License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=(
        'requests',
    ),
)