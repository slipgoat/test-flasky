import allure
import pytest

from core.clients.api_client import ApiClient
from core.entities.user import User


@pytest.fixture(scope="function")
@allure.step("Create only registered user")
def user_not_logged_in(api_client: ApiClient) -> User:
    return User.create_without_login()
