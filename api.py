from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:7000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    description: str | None = None

@app.get("/")
def connect_test(text: str, age):
    return {"message": f"Hello from document search with {text, age}"}

@app.post("/request")
def test_post(item : Item):
    print(item, "recived")
    return {"message": "Message recived"}
