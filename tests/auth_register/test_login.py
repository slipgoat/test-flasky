import allure
import pytest
from assertpy import soft_assertions

from core.models.base_models import Status, ApiErrorModel
from core.test_data.assertions import assert_that
from core.test_data.expectations import invalid_alphanumeric_field_values


@allure.feature("Log In")
class TestLogin:
    @allure.title("Success log in")
    def test_login_success(self, user_not_logged_in):
        response = user_not_logged_in.api.login(username=user_not_logged_in.username, password=user_not_logged_in.password)
        with soft_assertions():
            assert_that(response.status, "status is success").is_equal_to(Status.SUCCESS)
            assert_that(response.token, "token is string").is_instance_of(str)

    @allure.title("Success twice log in")
    def test_twice_login(self, user_not_logged_in):
        response = user_not_logged_in.api.login(username=user_not_logged_in.username, password=user_not_logged_in.password)
        response_2 = user_not_logged_in.api.login(username=user_not_logged_in.username, password=user_not_logged_in.password)
        with soft_assertions():
            assert_that(response_2.status, "status is success").is_equal_to(Status.SUCCESS)
            assert_that(response_2.token, "token is not the same").is_not_equal_to(response.token)

    @allure.title("Failure log in with wrong username")
    def test_login_failure_wrong_username(self, user_not_logged_in):
        response = user_not_logged_in.api.login(username="wrongusername", password=user_not_logged_in.password, response_code=401)
        self._check_401_response(response, "Invalid User")

    @allure.title("Failure log in with wrong password")
    def test_login_failure_wrong_password(self, user_not_logged_in):
        response = user_not_logged_in.api.login(username=user_not_logged_in.username, password="wrongpassword", response_code=401)
        self._check_401_response(response, "Invalid Authentication")

    @allure.step("Check 401 response")
    def _check_401_response(self, response: ApiErrorModel, message):
        with soft_assertions():
            assert_that(response.status, "status is failure").is_equal_to(Status.FAILURE)
            assert_that(response.message, f"message is '{message}'").is_equal_to(message)

    @pytest.mark.parametrize(
        "username", invalid_alphanumeric_field_values
    )
    @allure.title("Fail log in with invalid username")
    def test_login_failure_invalid_username(self, username, user_not_logged_in):
        response = user_not_logged_in.api.login(username, user_not_logged_in.password, response_code=400)
        assert_that(response.status, "status is failure").is_equal_to(Status.FAILURE)

    @pytest.mark.parametrize(
        "password", invalid_alphanumeric_field_values
    )
    @allure.title("Fail log in with invalid password")
    def test_login_failure_invalid_password(self, password, user_not_logged_in):
        response = user_not_logged_in.api.login(user_not_logged_in.username, password, response_code=400)
        assert_that(response.status, "status is failure").is_equal_to(Status.FAILURE)
