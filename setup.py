from setuptools import setup, find_packages

setup(
    name="AutoEDA",
    version="0.1.0",
    author="Harshal",
    description="Automated Exploratory Data Analysis with interactive HTML reports.",
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