from pydantic import BaseModel , Field
from typing import Optional


class CostCreate(BaseModel):
    
    description : str =  Field(min_length=3,max_length=100 , pattern = r"^[a-zA-Z0-9\- ]+$")
    amount : float = Field(ge=0)
    
class CostUpdate(BaseModel):
    description : Optional[str] =Field(default=None,min_length=3 , max_length=100, pattern = r"^[a-zA-Z0-9\- ]+$")
    amount : Optional[float] =Field(default=None ,ge=0)
    
    
class CostResponse(CostCreate):
    id : int 