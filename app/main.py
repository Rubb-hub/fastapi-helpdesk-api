from fastapi import FastAPI

from app.routers import auth, incidents

app = FastAPI()
app.include_router(incidents.router)
app.include_router(auth.router)
