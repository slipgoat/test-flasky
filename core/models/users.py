from typing import Optional

import names
from pydantic import BaseModel, Field

from core.models.base_models import ApiBaseModel, CreateBaseModel
from core.utils.utils import generate_string


class Users(ApiBaseModel):
    payload: list[str] = Field(...)


class UserPayload(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    phone: str = Field(...)


class User(ApiBaseModel):
    message: str = Field(...)
    payload: UserPayload = Field(...)


class RegisteredUpdatedUser(ApiBaseModel):
    message: str = Field(...)


class UpdateUserModel(CreateBaseModel):
    firstname: Optional[str] = Field(default_factory=lambda: names.get_first_name())
    lastname: Optional[str] = Field(default_factory=lambda: names.get_last_name())
    phone: Optional[str] = Field(default_factory=lambda: generate_string(letters=False, length=8))


class CreateUserModel(CreateBaseModel):
    username: Optional[str] = Field(default_factory=lambda: generate_string())
    password: Optional[str] = Field(default_factory=lambda: generate_string())
    firstname: Optional[str] = Field(default_factory=lambda: names.get_first_name())
    lastname: Optional[str] = Field(default_factory=lambda: names.get_last_name())
    phone: Optional[str] = Field(default_factory=lambda: generate_string(letters=False, length=8))


