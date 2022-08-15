import allure
import pytest
from assertpy import soft_assertions

from core.clients.api_client import ApiClient
from core.models.base_models import Status, ApiErrorModel
from core.models.users import CreateUserModel
from core.test_data.assertions import assert_that
from core.test_data.expectations import invalid_alphanumeric_field_values, invalid_numeric_field_values


@allure.feature("Registration")
class TestRegister:
    @allure.title("Success register")
    def test_register_success(self, api_client):
        data = CreateUserModel.create().dict()
        response = api_client.register(json_data=data)
        with soft_assertions():
            assert_that(response.message, "message is created").is_equal_to("Created")
            assert_that(response.status, "status is success").is_equal_to(Status.SUCCESS)

    @allure.title("Fail register existing user")
    def test_register_failure_existing_user(self, user, api_client):
        data = CreateUserModel.create(username=user.username).dict()
        response: ApiErrorModel = api_client.register(json_data=data, response_code=400)
        with soft_assertions():
            assert_that(response.status, "status is failure").is_equal_to(Status.FAILURE)
            assert_that(response.message, "message is 'User exists'").is_equal_to("User exists")

    @pytest.mark.parametrize(
        "field_name", ["username", "password", "firstname", "lastname", "phone"]
    )
    @allure.title("Fail register with missing field")
    def test_register_failure_missing_field(self, field_name, api_client):
        data = CreateUserModel.create().dict()
        del data[field_name]
        response = api_client.register(json_data=data, response_code=400)
        with soft_assertions():
            assert_that(response.status, "status is failure").is_equal_to(Status.FAILURE)
            assert_that(response.message, "message is 'Field missing'").is_equal_to("Field missing")

    @allure.title("Fail register with extra field")
    def test_register_failure_extra_field(self, api_client):
        data = CreateUserModel.create().dict()
        data.update({"extrafield": "some value"})

        response = api_client.register(json_data=data, response_code=400)
        with soft_assertions():
            assert_that(response.status, "status is failure").is_equal_to(Status.FAILURE)
            assert_that(response.message, "message is 'Invalid field'").is_equal_to("Invalid field")

    @allure.title("Fail register with not json data type")
    def test_register_failure_not_json_payload(self, api_client):
        data = "just text"

        response = api_client.register_not_json(data=data, response_code=400)
        with soft_assertions():
            assert_that(response.status, "status is failure").is_equal_to(Status.FAILURE)
            assert_that(response.message, "message is 'Bad request'").is_equal_to("Bad request")

    # #################
    # There are no specific requirements for these fields and the app lets to provide anything
    # so I put some basic options here for example
    # Validation in that case should be discussed with team and/or gathered from business/tech requirements
    @pytest.mark.parametrize(
        "username", invalid_alphanumeric_field_values
    )
    @allure.title("Fail register with invalid username")
    def test_register_failure_invalid_username(self, username, api_client):
        self._test_register_failure_invalid_field(api_client, CreateUserModel.create(username=username).dict())

    @pytest.mark.parametrize(
        "password", invalid_alphanumeric_field_values
    )
    @allure.title("Fail register with invalid password")
    def test_register_failure_invalid_password(self, password, api_client):
        self._test_register_failure_invalid_field(api_client, CreateUserModel.create(password=password).dict())

    @pytest.mark.parametrize(
        "firstname", invalid_alphanumeric_field_values
    )
    @allure.title("Fail register with invalid firstname")
    def test_register_failure_invalid_firstname(self, firstname, api_client):
        self._test_register_failure_invalid_field(api_client, CreateUserModel.create(firstname=firstname).dict())

    @pytest.mark.parametrize(
        "lastname", invalid_alphanumeric_field_values
    )
    @allure.title("Fail register with invalid lastname")
    def test_register_failure_invalid_lastname(self, lastname, api_client):
        self._test_register_failure_invalid_field(api_client, CreateUserModel.create(lastname=lastname).dict())

    @pytest.mark.parametrize(
        "phone", invalid_numeric_field_values
    )
    @allure.title("Fail register with invalid phone")
    def test_register_failure_invalid_phone(self, phone, api_client):
        self._test_register_failure_invalid_field(api_client, CreateUserModel.create(phone=phone).dict())

    def _test_register_failure_invalid_field(self, api_client: ApiClient, data: dict):
        response = api_client.register(json_data=data, response_code=400)
        with soft_assertions():
            assert_that(response.status, "status is failure").is_equal_to(Status.FAILURE)
