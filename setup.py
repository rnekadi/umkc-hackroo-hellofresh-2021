from setuptools import setup, find_packages

setup(
    name="raju-umkc-hellofresh-2021",
    version="0.0.1",
    author="Raju Nekadi",
    author_email="raju.nekadi08@gmail.com",
    description="HelloFresh UMKC HackRoo Spring 2021 Package",
    license='MIT',
    long_description_content_type="text/markdown",
    url="https://github.com/rnekadi/umkc-hackroo-hellofresh-2021",
    project_urls={
        "Project Github": "https://github.com/rnekadi/umkc-hackroo-hellofresh-2021",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
)