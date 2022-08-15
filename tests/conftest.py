import allure
import pytest

from core.clients.api_client import ApiClient
from core.entities.user import User


@pytest.fixture(scope="function")
@allure.step("Get Api Client")
def api_client():
    return ApiClient()


@pytest.fixture(scope="function")
@allure.step("Create user")
def user() -> User:
    return User.create()


@pytest.fixture(scope="function")
@allure.step("Create user_2")
def user_2() -> User:
    return User.create()
