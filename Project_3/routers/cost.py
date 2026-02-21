from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.cost import Cost
from schemas.cost import CostCreate, CostResponse

router = APIRouter(
    prefix="/costs",
    tags=["Costs"]
)

@router.post("/", response_model=CostResponse, status_code=201)
def create_cost(cost: CostCreate, db: Session = Depends(get_db)):
    db_cost = Cost(**cost.model_dump())
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    return db_cost