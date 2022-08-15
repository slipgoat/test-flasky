from enum import Enum
from typing import Type, TypeVar, Optional, Union, Callable

from pydantic import BaseModel as PydanticBaseModel, Extra, Field

T = TypeVar('T', bound=PydanticBaseModel)


class Status(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class Request(PydanticBaseModel):
    method: str
    path: str
    params: Optional[dict] = None
    data: Union[str, dict, list[dict], list[tuple], None] = None
    json_data: Union[dict, list[dict], None] = None
    headers: Optional[dict] = {}
    auth: Optional[tuple] = None
    timeout: Optional[int] = None
    parser: Optional[Callable] = None
    response_code: int = None


class CreateBaseModel(PydanticBaseModel):
    @classmethod
    def create(cls: Type[T], **kwargs):
        return cls(**kwargs)

    def dict_without_none(self) -> dict:
        dict_model = self.dict()
        output_dict = dict_model.copy()
        for k in dict_model.keys():
            if dict_model[k] is None:
                del output_dict[k]
        return output_dict


class BaseModel(PydanticBaseModel):
    class Config:
        extra = Extra.forbid
        underscore_attrs_are_private = True

    @classmethod
    def from_dict(cls: Type[T], dict_model: dict):
        return cls(**dict_model)


class ApiBaseModel(BaseModel):
    status: Status = Field(...)


class ApiErrorModel(BaseModel):
    message: str = Field(...)
    status: Status = Field(...)
