from typing import Optional, Union, IO
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi import Form
from dotenv import load_dotenv
from llm2server import cat_recognize
import uuid
import boto3
from sqlmodel import SQLModel, Field, Session, create_engine

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

s3 = boto3.client('s3',
  endpoint_url = os.getenv("AWS_ENDPOINT"),
)

class Cat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    breed: str
    remark:str
    image_url: str

def store_image(file: IO, filename:str) -> str:
    ext = filename.split(".")[-1]
    if ext.lower() not in ["jpg", "jpeg", "png", "gif"]:
        raise HTTPException(status_code=400, detail="Invalid image format")
    # UUID
    filename = f"{str(uuid.uuid4())}.{ext}" 
    s3.upload_fileobj(file, "cat-album", filename)
    public_domain = os.getenv("AWS_PUBLIC_DOMAIN")
    return f"{public_domain}/{filename}"


@app.put("/cat", response_model=Cat)
def add_cat(
    name: str = Form(...),
    breed: str = Form(...),
    remark: str = Form(...),
    image: UploadFile = File(...)
) -> Cat:
    assert image is not None, "Image file is required"
    assert image.filename != "", "Image filename is required"
    image_url = store_image(image.file, image.filename)
    cat = Cat(name=name, breed=breed, remark=remark, image_url=image_url)
    # store to database here
    with Session(engine) as session:
        session.add(cat)
        session.commit()
        session.refresh(cat)
    
    return cat
     

@app.get("/")
def read_root():
    return {"Hello": "World333"}

@app.get("/health")
def health_check():
    return "I'm Health!!!"

@app.get("/cat-name")
def get_cat_name(date:str):
    if date is None or date is "":
        return "小白"
        
    cat_names = {
        "11-17": "豆豆",
        "11-18": "黑黑",
        "11-19": "花花"
    }
    if date not in cat_names:
        return "小白"
    return cat_names[date]

@app.post("/cat-breed",) 
async def get_cat_breed(catImg:UploadFile=File(...)) -> str:

    cat_breed=await cat_recognize(catImg)
    return cat_breed