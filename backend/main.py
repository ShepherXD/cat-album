from typing import Union
from fastapi.middleware.cors import CORSMiddleware


from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
from llm2server import cat_recognize

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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