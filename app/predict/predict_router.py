import numpy as np
import joblib
from pydantic import BaseModel, Field
from fastapi import APIRouter


router = APIRouter()
loaded_model = joblib.load('models/model.pkl')


class InputModel(BaseModel):
    """input parameter"""
    plantcode_L: int = Field(default=0)
    week_no: int = Field(default=36)
    waitingno: int = Field(default=73)
    week_in: int = Field(default=1)
    dayno: int = Field(default=7)
    daytype: int = Field(default=2)
    regisecond: int = Field(default=44735)
    teamahead: int = Field(default=6)
    customercnt: int = Field(default=2)
    customergroupcnt: int = Field(default=2)
    seat_2: int = Field(default=24)
    seat_4: int = Field(default=34)
    seat_6: int = Field(default=18)
    seat_8: int = Field(default=0)
    seat_12: int = Field(default=3)
    temp_avg: float = Field(default=25.8)
    rainfall_amt: float = Field(default=0.0)
    humidity: float = Field(default=66.3)


class OutputModel(BaseModel):
    """response body"""
    predict: float = Field(
        2884.167288531745,
        description="wating time predict result"
        )


@router.post("/predict", response_model=OutputModel)
async def predict_wating_time(payload: InputModel) -> float:
    """predict waiting time router"""
    payload_values = list(payload.__dict__.values())
    input_data = np.array([payload_values])
    predict = loaded_model.predict(
        input_data,
        num_iteration=loaded_model.best_iteration
        )
    return {"predict": predict[0]}
