from pydantic import Field

from core.models.base_models import ApiBaseModel


class Token(ApiBaseModel):
    token: str = Field(...)
