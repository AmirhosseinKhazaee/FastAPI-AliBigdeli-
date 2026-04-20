from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_swagger import patch_fastapi
from fastapi.middleware.gzip import GZipMiddleware
from routers.task import router as task_router
from routers.auth import router as auth_router
from core.deps import get_current_user
from models.user import UserModel
from middleware.test import TestMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
scheduler = AsyncIOScheduler()



@asynccontextmanager
async def lifespan(app : FastAPI):
    print("Application Started")
    scheduler.add_job(my_task , IntervalTrigger(seconds=10))
    scheduler.start()
    yield
    scheduler.shutdown()
    print("Application Shutdown")

app = FastAPI(lifespan=lifespan,docs_url=None, swagger_ui_oauth2_redirect_url=None)
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


from fastapi import BackgroundTasks
from time import sleep, strftime


def async_task():
    print("hello")
    sleep(3)
    print("finished")


@app.get("/async")
async def try_async(background_tasks: BackgroundTasks):
    background_tasks.add_task(async_task)
    return {"message": "task added"}


def my_task():
    print(f"Task excuted at {strftime('%Y-%m-%d %H:%M:%S')}")
