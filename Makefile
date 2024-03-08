LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:="etl:${LOCAL_TAG}"
CONDA_ENV_NAME := "data_pipeline_pragma"
PYTHON_VERSION := "3.10"
ACTIVATE_ENV_SCRIPT := activate $(CONDA_ENV_NAME)


create_conda_env:
	conda create --name $(CONDA_ENV_NAME) python=$(PYTHON_VERSION)
	. $$(conda info --base)/etc/profile.d/conda.sh && conda activate $(CONDA_ENV_NAME)

activate_conda_env:
	. $$(conda info --base)/etc/profile.d/conda.sh && conda activate $(CONDA_ENV_NAME)


install_requeriments:
	pip install -r requirements.txt

setup:
	pre-commit install


quality_checks:
	isort  .
	black --config pyproject.toml **/*.py
	pylint --recursive=true .

test:
	pytest tests/

build: quality_checks test
	docker build -t ${LOCAL_IMAGE_NAME} .

integration_test: build
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash tests/integraton/run.sh

publish: build integration_test
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash scripts/publish.sh
