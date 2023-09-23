import json
import joblib
from datetime import datetime
import numpy as np
from pydantic import BaseModel, Field
from fastapi import APIRouter, Request
from app.utils.logger_utils import Logger


router = APIRouter()
MODEL = joblib.load('models/model.pkl')
LOGGER = Logger()


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
async def predict_wating_time(
    payload: InputModel,
    request: Request
    ) -> float:
    """predict waiting time router"""
    data = payload.__dict__
    uuid = request.cookies["visitor_id"]
    await logging(data, uuid)
    # make input data
    payload_values = list(data.values())
    input_data = np.array([payload_values])
    # execute predict
    predict = MODEL.predict(
        input_data,
        num_iteration=MODEL.best_iteration
        )
    response_body = {"predict": predict[0]}
    return response_body


async def logging(data: dict, uuid: str) -> None:
    """logging json body"""
    data["uuid"] = uuid
    data["timestamp"] = str(datetime.now())
    LOGGER().info(json.dumps(data, ensure_ascii=False))
    data.pop("uuid")
    data.pop("timestamp")
