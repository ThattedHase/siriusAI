from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from datetime import datetime
from catboost import CatBoostClassifier
import numpy as np
from const import MODEL_KEYS

model = CatBoostClassifier()
model.load_model("./model.cbm")

THRESHOLD = 0.2

class FormData(BaseModel):
    dob: str
    gender: str
    complaints: str
    diseases: Optional[str] = None
    surgeries: Optional[str] = None
    meds: Optional[str] = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

THRESHOLD = 0.2

@app.post("/suggest/")
async def suggest(data: FormData) -> list[str]:
    dob = datetime.strptime(data.dob, "%Y-%m-%d")
    now = datetime.now()
    age = (now - dob).days
    predict = model.predict_proba([
        (age - 3) / 44811,
        int(data.gender),
        data.complaints,
        data.diseases if data.diseases else "Факт получения травм, ожогов, ран, проведения медицинских манипуляций (инъекций, стоматологических, хирургических вмешательств и др.) в течение последних 30 дней отрицает, установление имплантата в течении 1 года отрицает. Перенесенные инфекционные заболевания, в т.ч. ВИЧ, вирусные гепатиты, туберкулез, COVID-19 отрицает.",
        data.surgeries if data.surgeries else "Отрицает",
        data.meds if data.surgeries else "Не отягощен"])
    indices = np.argsort(-predict)[:3]
    result = [MODEL_KEYS[indices[0]]]
    if predict[indices[1]] > THRESHOLD:
        result.append(MODEL_KEYS[indices[1]])
    if predict[indices[2]] > THRESHOLD:
        result.append(MODEL_KEYS[indices[2]])
    return result
