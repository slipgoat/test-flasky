from functools import partial
from typing import TypeVar, Type, Union
from urllib.parse import urljoin

import allure
from requests import Session, Response

from core.clients.middlewares import allure_attachments_middleware, logs_middleware
from core.models.base_models import ApiBaseModel, ApiErrorModel, Request
from core.models.token import Token
from core.models.users import Users, User, RegisteredUpdatedUser
from core.test_data.assertions import assert_that
from core.utils.utils import get_response_content

T = TypeVar("T", bound=ApiBaseModel)


class ApiClient(Session):
    def __init__(self,
                 base_path: str = "http://127.0.0.1:8080/api/",
                 token: str = None,
                 middlewares = None):
        super(ApiClient, self).__init__()
        self.base_path = base_path
        self.token = token
        self.middlewares = middlewares if middlewares is not None else [logs_middleware, allure_attachments_middleware]

    @allure.step("Log In")
    def login(self, username: str, password: str, response_code: int = 200) -> Union[Token, ApiErrorModel]:
        request = Request(
            method="GET",
            path="auth/token",
            auth=(username, password),
            parser=Token.from_dict,
            response_code=response_code,
        )
        return self._execute(request)

    @allure.step("Register")
    def register(self, json_data: dict, response_code: int = 201) -> Union[RegisteredUpdatedUser, ApiErrorModel]:
        request = Request(
            method="POST",
            path="users",
            json_data=json_data,
            parser=RegisteredUpdatedUser.from_dict,
            response_code=response_code,
        )
        return self._execute(request)

    # use only for negative tests
    @allure.step("Register with not json data type")
    def register_not_json(self, data: str, response_code: int = 400) -> ApiErrorModel:
        request = Request(
            method="POST",
            path="users",
            data=data,
            response_code=response_code,
        )
        return self._execute(request)

    @allure.step("Get users")
    def get_users(self, response_code: int = 200) -> Union[Users, ApiErrorModel]:
        request = Request(
            method="GET",
            path="users",
            parser=Users.from_dict,
            response_code=response_code,
        )
        return self._execute(request)

    @allure.step("Get user {username}")
    def get_user(self, username: str, response_code: int = 200) -> Union[User, ApiErrorModel]:
        request = Request(
            method="GET",
            path=f"users/{username}",
            parser=User.from_dict,
            response_code=response_code,
        )
        return self._execute(request)

    @allure.step("Update user {username}")
    def update_user(self, username: str, json_data: dict, response_code: int = 201) -> Union[RegisteredUpdatedUser, ApiErrorModel]:
        request = Request(
            method="PUT",
            path=f"users/{username}",
            json_data=json_data,
            parser=RegisteredUpdatedUser.from_dict,
            response_code=response_code,
        )
        return self._execute(request)

    # use only for negative tests
    @allure.step("Update user {username} with not json data type")
    def update_user_not_json(self, username: str, data: str, response_code: int = 400) -> ApiErrorModel:
        request = Request(
            method="PUT",
            path=f"users/{username}",
            data=data,
            response_code=response_code,
        )
        return self._execute(request)

    def _execute(self, request: Request) -> Union[Type[T], dict, str]:
        handler = self._execute_raw
        for middleware in self.middlewares:
            handler = partial(middleware, handler)

        updated_request = request.copy()
        updated_request.headers.update(self.headers)
        if self.token is not None:
            updated_request.headers.update({"Token": self.token})

        response = handler(updated_request)

        parser = updated_request.parser
        if response.status_code not in range(200, 400):
            parser = ApiErrorModel.from_dict

        response_content = get_response_content(response)
        return parser(response_content) if parser is not None else response_content

    def _execute_raw(self, request: Request) -> Response:
        url = urljoin(self.base_path, request.path)

        response = super(ApiClient, self).request(
            method=request.method,
            url=url,
            params=request.params,
            data=request.data,
            json=request.json_data,
            headers=request.headers,
            auth=request.auth,
            timeout=request.timeout or 10,
        )

        if request.response_code is not None:
            assert_that(response.status_code, f"response code is {request.response_code}")\
                .is_equal_to(request.response_code)

        return response
