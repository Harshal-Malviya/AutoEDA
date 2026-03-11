# AutoEDA

**AutoEDA** is a lightweight Python library that automatically performs **Exploratory Data Analysis (EDA)** and generates an **interactive HTML report** with visualizations, insights, and dataset statistics.

It is designed to help data scientists quickly understand a dataset without writing repetitive EDA code.

---

## Features

* Automatic dataset overview
* Missing value analysis
* Correlation matrix
* Distribution plots
* Boxplots
* Scatterplots
* Outlier detection
* Automated insights
* Interactive HTML dashboard
* Works in **Jupyter, Google Colab, Kaggle, and Python scripts**
* CLI support

---

## Installation

Install from PyPI:

```bash
pip install autoeda-pro
```

---

## Quick Start

```python
import pandas as pd
from autoeda import autoeda

df = pd.read_csv("data.csv")

a = autoeda(df)
a.analyze()
a.show()
```

This will generate a full interactive EDA report inside the notebook.

---

## Example Output

The generated report includes:

* Dataset overview
* Missing value statistics
* Correlation heatmap
* Variable distributions
* Boxplots and scatterplots
* Key insights about the dataset

---

## Export Report

You can export the report as a PDF by clicking on the "Download PDF" at the right corner of the report or you can also export the report as an HTML file: 

```python
a.save_html("report.html")
```

---

## Command Line Usage

AutoEDA also provides a CLI tool.

```bash
autoeda dataset.csv
```

This will generate:

```
autoeda_report.html
```

---

## Example Dataset

```python
import pandas as pd
from autoeda import autoeda

df = pd.read_csv("emissions_reduction_data.csv")

autoeda(df).analyze().show()
```

---

## Requirements

* Python ≥ 3.8
* pandas
* numpy
* matplotlib
* jinja2
* tqdm

---

## PyPI Package

Install the latest version:

```
pip install autoeda-pro
```

PyPI page:

https://pypi.org/project/autoeda-pro/

---

## Author

Harshal

---

## License

MIT License
