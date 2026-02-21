from sqlalchemy.orm import Session
from models.cost import Cost
from schemas.cost import CostCreate, CostUpdate
from fastapi import HTTPException, status


def create_cost(cost: CostCreate, db: Session):
    db_cost = Cost(**cost.model_dump())
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    return db_cost


def get_all_costs(db: Session):
    return db.query(Cost).all()


def get_cost_by_id(db: Session, cost_id: int):
    cost = db.query(Cost).filter(Cost.id == cost_id).first()
    if not cost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found"
        )
    return cost


def delete_cost(db: Session, cost_id: int):
    cost = db.query(Cost).filter(Cost.id == cost_id).first()
    if not cost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found"
        )
    db.delete(cost)
    db.commit()
    return {"detail": "Cost deleted"}


def update_cost(db: Session, cost_id: int, cost_data: CostUpdate):
    cost = get_cost_by_id(db, cost_id)
    update_data = cost_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data to update"
        )

    for key, value in update_data.items():
        setattr(cost, key, value)

    db.commit()
    db.refresh(cost)
    return cost
