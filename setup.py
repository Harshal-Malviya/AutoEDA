from setuptools import setup, find_packages

setup(
    name="autoeda-pro",
    version="0.1.3", 
    author="Harshal",
    description="Automated Exploratory Data Analysis with interactive HTML reports.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "jinja2",
        "tqdm"
    ],
    entry_points={
        "console_scripts": [
            "autoeda=autoeda.cli:main"
        ]
    },
    python_requires=">=3.8",
)