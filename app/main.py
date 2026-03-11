from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

data_username = "Coco"
data_password = "123"

class UserCreate(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# Vous implémentez une API REST avec FastAPI, qui contient un endpoint :
# POST /signin {username: string, password: string}
# et qui retourne { success: true | false } si la pair username/password 
# correspond à ce que vous écris en dur dans le code
@app.post("/signin/")
async def send_item(user_data: UserCreate):
    username = user_data.username
    password = user_data.password
    return {"Success": username == data_username and password== data_password}