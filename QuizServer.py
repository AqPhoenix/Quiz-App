from typing import Optional
from unicodedata import category
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import json

# generate custom id for each quiz
def id_gen():
    pass
# QUIZ structure
class answer_parm(BaseModel):
    answer_type: Optional[str] = "choice"
    answer_required: Optional[bool] = True

class Question(BaseModel):
    q_id: int
    question: str
    answer_parms: answer_parm
    answer_option: Optional[list] = []
    correct_answer: Optional[str] = ""

class Quiz(BaseModel):
    title: str
    author: str
    version: Optional[int] = 1
    category: Optional[list] = ["Quiz"]
    quiz: Optional[list] = [Question(
        q_id=0,
        question="What color is first in rainbow?",
        answer_parms=answer_parm(),
        answer_option = ["red","blue","green"],
        correct_answer="red"
        )
        ]
# END

quiz_inventory = []

app = FastAPI()

@app.get("/quiz")
def home():
    if len(quiz_inventory) != 0: return quiz_inventory
    else: return {"QUIZ":None}


@app.post("/add-quiz/", response_model=Quiz)
async def create_item(item: Quiz):
    quiz_inventory.append(jsonable_encoder(item))
    with open("data.json",'w') as f:
        f.write(json.dumps(quiz_inventory))
    return item