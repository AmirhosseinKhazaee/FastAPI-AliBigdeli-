from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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
    raise HTTPException(status_code=404, detail="Cost not found")

@app.get("/health")
def health_check():
    return JSONResponse({"status": "healthy"})

@app.get("/costs")
def get_all():
    return JSONResponse(costs)

@app.get("/costs/{id}")
def get_byid(id: int):
    return find_byid(id)

@app.post("/costs")
def add_cost(description: str, amount: float):
    new_cost = {
        "id": generate_id(),
        "description": description,
        "amount": amount
    }
    costs.append(new_cost)
    return new_cost

@app.put("/costs/{id}")
def edit_byid(id: int, description: str, amount: float):
    cost = find_byid(id)
    cost["description"] = description
    cost["amount"] = amount
    return cost
