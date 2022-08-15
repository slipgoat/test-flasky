import allure
import pytest
from assertpy import soft_assertions

from core.models.base_models import Status
from core.test_data.assertions import assert_that
from core.test_data.expectations import invalid_token_values


@allure.feature("Users")
class TestUsers:
    @allure.title("Get users")
    def test_get_users(self, user, user_2, api_client):
        response = api_client.get_users()
        with soft_assertions():
            assert_that(response.status, "status is success").is_equal_to(Status.SUCCESS)
            assert_that(response.payload, "payload contains registered users").contains(user.username, user_2.username)

    @allure.title("Get user")
    def test_get_user(self, user):
        response = user.api.get_user(username=user.username)
        assert_that(response, "response is correct").is_equal_to({
            "status": Status.SUCCESS,
            "message": "retrieval succesful",
            "payload": {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "phone": user.phone
            }
        })

    @allure.title("Get other user")
    def test_get_other_user(self, user, user_2):
        response = user.api.get_user(username=user_2.username)
        assert_that(response, "response is correct").is_equal_to({
            "status": Status.SUCCESS,
            "message": "retrieval succesful",
            "payload": {
                "firstname": user_2.firstname,
                "lastname": user_2.lastname,
                "phone": user_2.phone
            }
        })

    @pytest.mark.parametrize(
        "token, message", invalid_token_values
    )
    @allure.title("Fail to get user with invalid token")
    def test_get_user_failure_invalid_token(self, token, message, user, api_client):
        api_client.token = token
        response = api_client.get_user(user.username, response_code=401)
        assert_that(response, "fail response is correct").is_equal_to(
            {
                "status": Status.FAILURE,
                "message": message
            }
        )

    @allure.title("Fail to get user with expired token")
    def test_get_user_failure_expired_token(self, user, api_client):
        api_client.token = user.token
        user.login()
        response = api_client.get_user(user.username, response_code=401)
        assert_that(response, "fail response is correct").is_equal_to(
            {
                "status": Status.FAILURE,
                "message": "Invalid Token"
            }
        )

    @allure.title("Fail to get not existing user")
    def test_get_not_existing_user(self, user):
        user.api.get_user(username="notexistinguser", response_code=404)

