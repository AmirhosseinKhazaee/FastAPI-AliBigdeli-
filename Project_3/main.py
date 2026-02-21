from fastapi import FastAPI, HTTPException ,status
from schemas.cost import CostCreate ,CostUpdate ,CostResponse
from core.database import Base, engine
from models import cost
from typing import List 
from routers.cost import router as cost_router

app = FastAPI()


app.include_router(cost_router)



