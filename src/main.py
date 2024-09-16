import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.database import engine
from src.models import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# importamos los routers desde nuestros modulos
from src.example.router import router as example_router

load_dotenv()
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    #"http://example.com",  # Add your frontend domain here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI with CORS!"}

ENV = os.getenv("ENV")
ROOT_PATH = os.getenv(f"ROOT_PATH_{ENV.upper()}")



@asynccontextmanager
async def db_creation_lifespan(app: FastAPI):
    BaseModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(root_path=ROOT_PATH, lifespan=db_creation_lifespan)

# asociamos los routers a nuestra app
app.include_router(example_router)
