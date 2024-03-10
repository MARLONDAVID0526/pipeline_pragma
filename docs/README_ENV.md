
# ETL Makefile

This Makefile provides a set of targets to manage testing, quality checks, building Docker images, integration testing, publishing, and setup for the ETL project.

## Targets

### Variables
```Makefile
LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:="etl:${LOCAL_TAG}"
CONDA_ENV_NAME := "data_pipeline"
PYTHON_VERSION := "3.12"
ACTIVATE_ENV_SCRIPT := activate $(CONDA_ENV_NAME)
```
```Makefile
create_conda_env:
	conda create --name $(CONDA_ENV_NAME) python=$(PYTHON_VERSION)
	. $$(conda info --base)/etc/profile.d/conda.sh && conda activate $(CONDA_ENV_NAME)


install_requeriments:
	pip install -r requirements.txt

setup:
	pre-commit install
```


To use the Makefile, execute the desired target using the make command followed by the target name. For example:


### requeriments
Create enviroments, by default python 3.12 and Condas enviroment called  data_pipeline.

```bash
make create_conda_env
```

### requeriments
Install requirements on the environment.
```bash
make install_requeriments
```


### setup
Install necessary pre-commit hooks.
```bash
make  setup

```



### quality_checks
Runs isort, black, and pylint for code quality checks.

```bash
Runs pytest for tests.
```

### build
Builds the Docker image after running quality checks and tests.

```bash
make build
```

### integration_test
Runs integration tests after building the Docker image.
```bash
make integration_test
```

###
Publishes the Docker image after building and running integration tests.
```bash
make  publish

```








# data_engineering
This repo is a base github repo, for implementing pipelines

# Requirements and Libraries

## Data Libraries

- **Pandas** (Version: 2.2.0)
  - [Documentation](https://pandas.pydata.org/)

- **DLT** (Version: 0.4.4)
  - [Documentation](https://dlthub.com/docs/intro)

## Parquet

- **PyArrow** (Version: 14.0.1)

## Environmental Variables

- **python-dotenv** (Version: 0.21.1)

## Libraries AWS

- **Boto3** (Version: 1.28.83)

## Libraries GCP

[Add libraries here if applicable]

## Libraries AZURE

[Add libraries here if applicable]


# Pre-commit

## Installation

1. Install `pre-commit` using pip:
    ```bash
    pip install pre-commit
    ```

2. Install the pre-commit hooks:
    ```bash
    pre-commit install
    ```

3. Generate a sample configuration file:
    ```bash
    pre-commit sample-config > .pre-commit-config.yaml
    ```

## Configuration

After generating the sample configuration file, you can replace `.pre-commit-config.yaml` with your desired configurations. Here's a sample configuration file:

```yaml
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v3.2.0
  hooks:
    - id: trailing-whitespace
    - id: end-of-file-fixer
    - id: check-yaml
    - id: check-added-large-files
- repo: https://github.com/psf/black
  rev: 22.6.0
  hooks:
    - id: black
      language_version: python3.11
- repo: local
  hooks:
    - id: pylint
      name: pylint
      entry: pylint
      language: system
      types: [python]
      args: [
        "-rn", # Only display messages
        "-sn", # Don't display the score
        "--recursive=y"
      ]
- repo: local
  hooks:
    - id: pytest-check
      name: pytest-check
      entry: pytest
      language: system
      pass_filenames: false
      always_run: true
      args: [
        "tests/"
      ]
- repo: https://github.com/pycqa/isort
  rev: 5.13.2
  hooks:
    - id: isort
      name: isort (python)

- repo: https://github.com/gitguardian/ggshield
  rev: v1.24.0
  hooks:
    - id: ggshield
      language_version: python3
      stages: [commit]

```
