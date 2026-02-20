from fastapi import FastAPI, HTTPException ,status
from models import CostCreate ,CostUpdate ,CostResponse
from typing import List 

app = FastAPI()

costs = []

def generate_id():
    if costs:
        return max(cost["id"] for cost in costs) + 1
    return 0

def find_byid(id: int):
    for cost in costs:
        if cost["id"] == id:
            return cost
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found")

@app.get("/health",status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy"}

@app.get("/costs",status_code=status.HTTP_200_OK, response_model=List[CostResponse])
def get_all():
    return costs

@app.get("/costs/{id}",status_code=status.HTTP_200_OK,response_model=CostResponse)
def get_byid(id: int):
    return find_byid(id)

@app.post("/costs" ,status_code=status.HTTP_201_CREATED, response_model=CostResponse)
def add_cost(cost : CostCreate):
    new_cost = {
        "id": generate_id(),
        "description": cost.description,
        "amount": cost.amount
    }
    costs.append(new_cost)
    return new_cost

@app.patch("/costs/{id}" ,status_code=status.HTTP_200_OK,response_model=CostResponse)
def edit_byid(id: int , cost : CostUpdate):
    existing_cost = find_byid(id)
    update_data = cost.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    existing_cost.update(update_data)
    return existing_cost