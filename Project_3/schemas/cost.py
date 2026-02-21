from pydantic import BaseModel, Field
from typing import Optional


class CostCreate(BaseModel):

    description: str = Field(
        min_length=3, max_length=100, pattern=r"^[a-zA-Z0-9\- ]+$", example="Type Here"
    )
    amount: float = Field(ge=0, example=12.5)


class CostUpdate(BaseModel):
    description: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
        pattern=r"^[a-zA-Z0-9\- ]+$",
        example="Type Here",
    )
    amount: Optional[float] = Field(default=None, ge=0, example=12.5)


class CostResponse(CostCreate):
    id: int
