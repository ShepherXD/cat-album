from enum import Enum
from typing import Optional, Union, IO
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi import Form
from fastapi import BackgroundTasks
from dotenv import load_dotenv
from pydantic import model_validator
from llm2server import cat_recognize
import uuid
import boto3
import time
from sqlmodel import SQLModel, Field, Session, create_engine, select

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
    analysis_task_id: Optional[int] = Field(default=None, foreign_key="breed_analysis_task.id")


class TaskStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class BreedAnalysisTask(SQLModel, table=True):
    __tablename__ = "breed_analysis_task"
    id: Optional[int] = Field(default=None, primary_key=True)
    status: TaskStatus = Field(default=TaskStatus.IN_PROGRESS)
    result: Optional[str] = Field(default=None)# breed result when completed
    
    @model_validator(mode='after')
    def check_consistency(self):
        if self.status == TaskStatus.COMPLETED and self.result is None:
            raise ValueError("Finished task must have a result")
        
        if self.status != TaskStatus.COMPLETED and self.result is not None:
            raise ValueError("Unfinished task cannot have a result")
        return self

def store_image(file: bytes, filename:str) -> str:
    ext = filename.split(".")[-1]
    if ext.lower() not in ["jpg", "jpeg", "png", "gif"]:
        raise HTTPException(status_code=400, detail="Invalid image format")
    filename = f"{str(uuid.uuid4())}.{ext}" 
    s3.put_object(
        Bucket=os.getenv("AWS_BUCKET_NAME"),
        Key=filename,
        Body=file,
        ContentType=f"image/{ext}",
    )
    public_domain = os.getenv("AWS_PUBLIC_DOMAIN")
    return f"{public_domain}/{filename}"


@app.put("/cat", response_model=Cat)
async def add_cat(
    background_tasks: BackgroundTasks,
    name: str = Form(None),
    breed: str = Form(None),
    remark: str = Form(None),
    image: UploadFile = File(...)
) -> Cat:
    assert image.filename is not None and image.filename != "", "Image filename is required"
    img_data = await image.read()
    image_url = store_image(img_data, image.filename)
    task_id = submit_breed_analysis(background_tasks, img_data)
    cat = Cat(
        name=name,
        breed=breed,
        remark=remark,
        image_url=image_url,
        analysis_task_id=task_id
    )

    with Session(engine) as session:
        session.add(cat)
        session.commit()
        session.refresh(cat)
    
    return cat

@app.patch("/cat/{cat_id}", response_model=Cat)
async def modify_cat(
    cat_id: int,
    background_tasks: BackgroundTasks,
    name: Optional[str] = Form(None),
    breed: Optional[str] = Form(None),
    remark: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
) -> Cat:
    with Session(engine) as session:
        cat = session.get(Cat, cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        
        if name is not None:
            cat.name = name
        if breed is not None:
            cat.breed = breed
        if remark is not None:
            cat.remark = remark
        if image is not None:
            assert image.filename is not None, "Image filename is required"
            img_data = await image.read()
            cat.image_url = store_image(img_data, image.filename)
            cat.analysis_task_id = submit_breed_analysis(background_tasks,img_data)
        
        session.add(cat)
        session.commit()
        session.refresh(cat)
    
    return cat

@app.get("/cat/{cat_id}", response_model=Cat)
def get_cat(cat_id: int) -> Cat:
    with Session(engine) as session:
        cat = session.get(Cat, cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
    return cat

@app.get("/cat", response_model=list[Cat])
def get_cat_list():
    with Session(engine) as session:
        cats = session.exec(
            select(Cat)
        ).all()
    return cats
     

@app.get("/")
def read_root():
    return {"Hello": "World333"}

@app.get("/health")
def health_check():
    return "I'm Health!!!"

@DeprecationWarning
@app.post("/cat-breed",) 
async def get_cat_breed_sync(
    catImg:UploadFile=File(...),
) -> str:
    cat_breed=cat_recognize(catImg)
    return cat_breed


def submit_breed_analysis(
    background_tasks: BackgroundTasks,
    img_data:bytes,
) -> int:
    task = BreedAnalysisTask(status=TaskStatus.IN_PROGRESS)
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        task_id = task.id
        assert task_id is not None
    # process the image in background
    def task_wrapper(img_data: bytes):
        try:
            breed = cat_recognize(img_data)
        except Exception as e:
            with Session(engine) as session:
                task = session.get(BreedAnalysisTask, task_id)
                if task is None:
                    print(f"Task with id {task_id} not found to mark as FAILED")
                    return 
                task.status = TaskStatus.FAILED
                session.add(task)
                session.commit()
                return
            
        with Session(engine) as session:
            task = session.get(BreedAnalysisTask, task_id)
            if task is None:
                print(f"Task with id {task_id} not found to mark as COMPLETED")
                return
            task.status = TaskStatus.COMPLETED
            task.result = breed
            session.add(task)
            session.commit()
        # update breed of cats associated with this task if exists
        with Session(engine) as session:
            cats = session.exec(
                select(Cat).where(Cat.analysis_task_id == task_id)
            ).all()
            assert len(cats) <=1, "Each task should be associated with at most one cat"
            if len(cats) == 1:
                cat = cats[0]
                cat.breed = breed
                session.add(cat)
                session.commit()
    background_tasks.add_task(task_wrapper, img_data)
    return task_id


    
    

@app.get("/cat-breed/task/{task_id}")
async def get_task_result(
    task_id: int,
):
    # if task is done, return result
    # else return the progress
    with Session(engine) as session:
        task = session.get(BreedAnalysisTask, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task