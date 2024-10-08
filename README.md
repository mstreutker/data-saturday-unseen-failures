# Data Saturday - Unseen Failures
An example project demonstrating how to develop and test a Python project locally using Spark.  
Special thanks to my colleagues [Jody](https://github.com/sqlkabouter) and [Wessel](https://github.com/TheScriptingGuy/docker-azure-spark) for contributing to this example.


# Introduction

This code sample belongs to the session  

Unseen Failures - Adventures in Data Pipeline Testing  

As presentated on
[Data Saturday Holland and Fabric Friday 2024](https://datasaturday.nl/).

Summary:

In today’s data-driven landscape, ensuring the reliability of data pipelines is a complex challenge. This presentation will give a brief overview of Test-Driven Development (TDD) and Behavior Driven Development (BDD) methodologies as key approaches to enhancing code quality and ensuring alignment with business requirements. Furthermore, the presentation will cover the growing importance of Data Observability, highlighting how it plays a crucial role in proactively monitoring and validating data flows. We will demonstrate the use of tools like pytest, behave, and Great Expectations to implement effective data testing and monitoring solutions.
Join this session to gain actionable insights and practical strategies to enhance the reliability of your data pipelines in the face of unpredictable data challenges.

# Quickstart

_How to use the project..._

- Install [Rancher Destkop](https://rancherdesktop.io/)
- Install [Visual Studio Code](https://code.visualstudio.com/)
- Install the extension [Visual Studio Code Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Install [Git for Windows](https://git-scm.com/download/win)
- Clone the repository

See [The Scripting Guy](https://github.com/TheScriptingGuy/docker-azure-spark?tab=readme-ov-file#how-can-you-use-this-project) on how to configure Rancher Desktop properly.

# Features

- [x] Develop and test locally using [Visual Studio Code Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [x] Run tests using [pytest](https://pypi.org/project/pytest/) and [behave](https://pypi.org/project/behave/) against Spark DataFrames and Delta tables
- [x] Run tests using [Great Expectations](https://greatexpectations.io/gx-core) against Spark DataFrames and Delta tables


# Run the demo
**Prerequisites**
- Start Rancher Desktop  
- Start VS Code
- Load the Unseen Failures folder
- Press F1 and choose  `Dev Containers - Open Folder in Container..`
- Open the `bash` terminal

**Unit Tests**  

To run the unit tests, run the following command in the project root:

```
pytest
```
**Behaviour Driven Design**  

To run the BDD tests, run the following command in the project root:

```
behave
```

**Great Expectations**  

To run the GX tests, run the following command in the project root:
```
python demo/great-expectations-demo.py 
```
By default, the testresults of Great Expectations will end up in `/demo/docs`