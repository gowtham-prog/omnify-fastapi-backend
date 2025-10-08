# app/main.py
from fastapi import FastAPI
from .routers import events, registrations
from .db import engine, Base
import asyncio
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Mini Event Management API")

origins = [
    "http://localhost:3000",       
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           
    allow_credentials=True,          # cookies, auth headers
    allow_methods=["*"],             # all HTTP methods
    allow_headers=["*"],             # all headers
)

app.include_router(events.router)
app.include_router(registrations.router)



# Optional startup hook to create tables in dev (use Alembic for prod/migrations)
@app.on_event("startup")
async def on_startup():
    # create tables if not present (convenience for local dev)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
