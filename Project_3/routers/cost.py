from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from schemas.cost import CostCreate, CostUpdate, CostResponse
from crud import cost as crud_cost  # import your crud layer

router = APIRouter(
    prefix="/costs",
    tags=["Costs"]
)

# -------------------------
# CREATE
# -------------------------
@router.post("/", response_model=CostResponse, status_code=status.HTTP_201_CREATED)
def create_cost(cost: CostCreate, db: Session = Depends(get_db)):
    return crud_cost.create_cost(db, cost)


# -------------------------
# GET ALL
# -------------------------
@router.get("/", response_model=List[CostResponse], status_code=status.HTTP_200_OK)
def get_all_costs(db: Session = Depends(get_db)):
    return crud_cost.get_all_costs(db)


# -------------------------
# GET BY ID
# -------------------------
@router.get("/{cost_id}", response_model=CostResponse, status_code=status.HTTP_200_OK)
def get_cost_by_id(cost_id: int, db: Session = Depends(get_db)):
    return crud_cost.get_cost_by_id(db, cost_id)


# -------------------------
# UPDATE (PATCH)
# -------------------------
@router.patch("/{cost_id}", response_model=CostResponse, status_code=status.HTTP_200_OK)
def update_cost(cost_id: int, cost_data: CostUpdate, db: Session = Depends(get_db)):
    return crud_cost.update_cost(db, cost_id, cost_data)


# -------------------------
# DELETE
# -------------------------
@router.delete("/{cost_id}", status_code=status.HTTP_200_OK)
def delete_cost(cost_id: int, db: Session = Depends(get_db)):
    return crud_cost.delete_cost(db, cost_id)