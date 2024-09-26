# local-pyspark
An example project demonstrating how to develop and test a Python project locally using Spark.

# Introduction

Over the past few years, data solutions have increasingly relied on major public cloud providers and SaaS vendors. We've grown used to the convenience of configuring and deploying Spark clusters and immediately beginning to write code in Notebooks. However, this shift has brought some challenges, including:

- Dependence on cloud solutions, where clusters need to be running for development and testing, potentially leading to additional costs.
- Difficulty in developing consistent, best-practice-compliant code across notebooks, developers and projects.

Additionally, we transitioned from the familiar SQL-based approach to a Python-based approach. While this offers significant advantages, such as enhanced capabilities for automated testing and validation of our solutions, it can also present a steep learning curve for those new to coding.

The local-pyspark project aims to provide guidelines and practical examples to help address these challenges.

> [!NOTE] 
> Since I'm primarily working with Microsoft Synapse Analytics and Microsoft Fabric at the moment, this project is focused on developing for these technology stacks. It hasn't yet been tested with other platforms like Databricks.

# Quickstart

_How to use the project..._

- Install [Rancher Destkop](https://rancherdesktop.io/)
- Install [Visual Studio Code](https://code.visualstudio.com/)
- Install the extension [Visual Studio Code Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Install [Git for Windows](https://git-scm.com/download/win)
- Clone the repository
- etc...

# Features

- [x] Develop and test locally using [Visual Studio Code Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [x] Validate code against best practices and errors and format the code for consistency using tools such as [ruff](https://pypi.org/project/ruff/) and [mypy](https://pypi.org/project/mypy/)
- [x] Run tests using [pytest](https://pypi.org/project/pytest/) and [behave](https://pypi.org/project/behave/) against Spark DataFrames and Delta tables
- [x] Configure the project, tools and build using [pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [x] All tools and extensions are preconfigured in the Dev Container and Visual Studio code settings
- [ ] A sample project focused on a practical data-driven solution, moving beyond basic examples like a calculator app.
- [ ] A sample CI/CD pipeline implemented with GitHub workflows.
- [ ] A sample CI/CD pipeline utilizing Azure DevOps multistage pipelines.
- [ ] Enhance the example with data quality checks and essential components for starting data observability.

# Tools and extensions

- Rancher Desktop
- Visual Studio Code
- Dev Containers

**Python**
- Ruff
- mypy
- pytest
- behave
- tox
