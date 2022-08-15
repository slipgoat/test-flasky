import allure
import pytest

from core.test_data.assertions import assert_that
from .data.expectations import expect_user
from core.models.base_models import Status
from core.models.users import UpdateUserModel
from core.test_data.expectations import invalid_alphanumeric_field_values, invalid_numeric_field_values, invalid_token_values


@allure.feature("Update Users")
class TestUpdateUsers:
    @allure.title("Full update user")
    def test_update_user_full(self, user):
        updated_data = UpdateUserModel.create()
        response = user.api.update_user(username=user.username, json_data=updated_data.dict())
        assert_that(response, "response is correct").is_equal_to({
            "status": Status.SUCCESS,
            "message": "Updated"
        })

        user_response = user.api.get_user(username=user.username)
        assert_that(user_response, "user data has been updated").is_equal_to(
            expect_user(firstname=updated_data.firstname, lastname=updated_data.lastname, phone=updated_data.phone)
        )

    @allure.title("Partially update user")
    def test_update_user_partially(self, user):
        updated_data = UpdateUserModel.create(firstname=None, lastname=None)
        updated_data_dict = updated_data.dict_without_none()
        response = user.api.update_user(username=user.username, json_data=updated_data_dict)
        assert_that(response, "response is correct").is_equal_to({
            "status": Status.SUCCESS,
            "message": "Updated"
        })

        user_response = user.api.get_user(username=user.username)
        assert_that(user_response, "user data has been updated").is_equal_to(
            expect_user(firstname=user.firstname, lastname=user.lastname, phone=updated_data.phone)
        )

    @allure.title("Update other user")
    def test_update_other_user(self, user, user_2):
        updated_data = UpdateUserModel.create()
        response = user.api.update_user(username=user_2.username, json_data=updated_data.dict())
        assert_that(response, "response is correct").is_equal_to({
            "status": Status.SUCCESS,
            "message": "Updated"
        })

        user_response = user.api.get_user(username=user.username)
        assert_that(user_response, "user_1 data hasn't been changed").is_equal_to(
            expect_user(firstname=user.firstname, lastname=user.lastname, phone=user.phone)
        )

        user_2_response = user.api.get_user(username=user_2.username)
        assert_that(user_2_response,"user_2 data has been updated").is_equal_to(
            expect_user(firstname=updated_data.firstname, lastname=updated_data.lastname, phone=updated_data.phone)
        )

    @allure.title("Fail to update not existing user")
    def test_update_failure_not_existing_user(self, user):
        updated_data = UpdateUserModel.create()
        user.api.update_user(username="notexistinguser", json_data=updated_data.dict(), response_code=404)

    @allure.title("Fail to update user with extra field")
    def test_update_user_failure_extra_field(self, user):
        updated_data = UpdateUserModel.create()
        updated_data_dict = updated_data.dict()
        updated_data_dict.update({"extrafield": "somevalue"})
        # not sure it is compatible response code - 403 - I'd expect 400
        response = user.api.update_user(username=user.username, json_data=updated_data_dict, response_code=403)
        assert_that(response, "fail response is correct").is_equal_to({
            "status": Status.FAILURE,
            "message": "Field update not allowed"
        })

        user_response = user.api.get_user(username=user.username)
        assert_that(user_response, "user data hasn't been changed").is_equal_to(
            expect_user(firstname=user.firstname, lastname=user.lastname, phone=user.phone)
        )

    @allure.title("Fail to update user with not json data type")
    def test_update_user_failure_not_json_data(self, user):
        updated_data = "someupdateddata"
        response = user.api.update_user_not_json(username=user.username, data=updated_data)
        assert_that(response, "fail response is correct").is_equal_to({
            "status": Status.FAILURE,
            "message": "Bad Request"
        })

    @pytest.mark.parametrize(
        "token, message", invalid_token_values
    )
    @allure.title("Fail to update user with invalid token")
    def test_update_user_failure_invalid_token(self, token, message, user, api_client):
        api_client.token = token
        updated_data = UpdateUserModel.create()
        response = api_client.update_user(username=user.username, json_data=updated_data.dict(), response_code=401)
        assert_that(response, "fail response is correct").is_equal_to(
            {
                "status": Status.FAILURE,
                "message": message
            }
        )

        user_response = user.api.get_user(username=user.username)
        assert_that(user_response, "user data hasn't been changed").is_equal_to(
            expect_user(firstname=user.firstname, lastname=user.lastname, phone=user.phone)
        )

    @allure.title("Fail to update user with expired token")
    def test_update_user_failure_expired_token(self, user, api_client):
        api_client.token = user.token
        user.login()
        updated_data = UpdateUserModel.create()
        response = api_client.update_user(username=user.username, json_data=updated_data.dict(), response_code=401)
        assert_that(response, "fail response is correct").is_equal_to(
            {
                "status": Status.FAILURE,
                "message": "Invalid Token"
            }
        )

        user_response = user.api.get_user(username=user.username)
        assert_that(user_response, "user data hasn't been changed").is_equal_to(
            expect_user(firstname=user.firstname, lastname=user.lastname, phone=user.phone)
        )

    @pytest.mark.parametrize(
        "firstname", invalid_alphanumeric_field_values
    )
    @allure.title("Fail to update user with invalid firstname")
    def test_login_failure_invalid_firstname(self, firstname, user):
        updated_data = UpdateUserModel.create(firstname=firstname)
        response = user.api.update_user(username=user.username, json_data=updated_data.dict(), response_code=400)
        assert_that(response.status, "status is failure").is_equal_to(Status.FAILURE)

    @pytest.mark.parametrize(
        "lastname", invalid_alphanumeric_field_values
    )
    @allure.title("Fail to update user with invalid lastname")
    def test_login_failure_invalid_lastname(self, lastname, user):
        updated_data = UpdateUserModel.create(lastname=lastname)
        response = user.api.update_user(username=user.username, json_data=updated_data.dict(), response_code=400)
        assert_that(response.status, "status is failure").is_equal_to(Status.FAILURE)

    @pytest.mark.parametrize(
        "phone", invalid_numeric_field_values
    )
    @allure.title("Fail to update user with invalid phone")
    def test_login_failure_invalid_lastname(self, phone, user):
        updated_data = UpdateUserModel.create(phone=phone)
        response = user.api.update_user(username=user.username, json_data=updated_data.dict(), response_code=400)
        assert_that(response.status, "status is failure").is_equal_to(Status.FAILURE)

