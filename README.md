## Run tests
Execute `./run.sh` to run tests

By default, debug logging is enabled

To generate allure report it needs to install allure cli here:

    https://docs.qameta.io/allure-report/#_installing_a_commandline

Execute `allure serve` to generate report

## Used dependencies:
- **python 3.9**
- **poetry** for dependencies management and virtual envs
- **pytest** as test runner
- **requests** for api requests execution
- **pydantic** for typing and work with models
- **names** for generate human-readable names
- **assertpy** for assertions
- **pytest-xdist** for tests parallel execution
- **allure-pytest** for generate report using allure framework

### Found bugs
1. Getting non-existent user returns 500 instead of 404 
2. Updating non-existent user returns 201 instead of 404. Actually, nothing is updated 
3. It is possible to register/log in/update with None values for all input fields
4. It is possible to register/log in/update with only non-punctuation symbols for all input fields 
5. It is possible to register/log in/update with only space symbols for all input fields 
6. It is possible to register/update with letter symbols for phone input field 
7. There are no other validation requirements for input fields so it should be discussed
