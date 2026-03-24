from fastapi import FastAPI, Depends
from fastapi_swagger import patch_fastapi
from routers.task import router as task_router
from routers.auth import router as auth_router
from core.deps import get_current_user
from models.user import UserModel

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app, docs_url="/swagger")


app.include_router(task_router)
app.include_router(auth_router)


@app.get("/public")
def public():
    return {"message": "this is public endpoint"}


@app.get("/private")
def private(user: UserModel = Depends(get_current_user)):
    return {"message": "this is private endpoint"}
