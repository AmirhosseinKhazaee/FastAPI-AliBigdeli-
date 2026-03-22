from fastapi import FastAPI, Depends
from fastapi_swagger import patch_fastapi
from routers.task import router as task_router

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app, docs_url="/swagger")


app.include_router(task_router)

from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()


@app.get("/public")
def public():
    return {"message": "this is public endpoint"}


@app.get("/private")
def private(credentials: HTTPBasicCredentials = Depends(security)):
    return {
        "message": "this is private endpoint",
        "user": credentials.username,
        "password": credentials.password,
    }
