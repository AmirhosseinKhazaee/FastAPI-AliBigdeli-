from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_swagger import patch_fastapi
from fastapi.middleware.gzip import GZipMiddleware
from routers.task import router as task_router
from routers.auth import router as auth_router
from core.deps import get_current_user
from models.user import UserModel
from middleware.test import TestMiddleware

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app, docs_url="/swagger")

app.include_router(task_router)
app.include_router(auth_router)


app.add_middleware(TestMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/public")
def public():
    return {"message": "this is public endpoint"}


@app.get("/private")
def private(user: UserModel = Depends(get_current_user)):
    return {"message": "this is private endpoint"}
