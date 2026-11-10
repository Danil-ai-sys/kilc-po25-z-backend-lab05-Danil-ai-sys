"""What the client may send: TaskIn and TaskPatch, Pydantic models. (M2, lessons 11 and 14)"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

Title = Annotated[str, Field(min_length=1, max_length=100)]


def _clean_title(v: str) -> str:
    v = v.strip()
    if not v:
        raise ValueError("title must not be blank")
    return v


class TaskIn(BaseModel):
    title: Title
    done: bool = False

    @field_validator("title")
    @classmethod
    def not_blank(cls, v: str) -> str:
        return _clean_title(v)


class TaskPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Title | None = None
    done: bool | None = None

    # Must stay ABOVE the strip validator: None.strip() would crash.
    @field_validator("title", "done")
    @classmethod
    def not_null(cls, v):
        if v is None:
            raise ValueError("may be left out, but not null")
        return v

    @field_validator("title")
    @classmethod
    def not_blank(cls, v: str) -> str:
        return _clean_title(v)
