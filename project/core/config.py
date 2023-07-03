from fastapi import FastAPI
from project.api.accounts_client import router

app = FastAPI()

app.include_router(router.router, tags=["accounts_client_api"])
