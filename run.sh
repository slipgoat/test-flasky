#!/bin/bash

pip3.9 install poetry
mkdir .venv && poetry config virtualenvs.in-project=true
poetry env use python3.9
source .venv/bin/activate
poetry update
rm -rf allure-*
pytest -n 5 --alluredir allure-results tests/
deactivate