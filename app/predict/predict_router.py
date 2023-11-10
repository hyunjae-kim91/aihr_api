import json
import joblib
from datetime import datetime
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from fastapi import APIRouter, Request
from scipy.special import inv_boxcox

from app.utils.logger_utils import Logger


router = APIRouter()
MODEL = joblib.load('models/model_lgbm.pkl')
LOGGER = Logger()


class InputModel(BaseModel):
    """input parameter"""
    plantcode_L: int = Field(default=0)
    week_no: int = Field(default=36)
    waitingno: int = Field(default=73)
    week_int: int = Field(default=1)
    dayno: int = Field(default=7)
    daytype: int = Field(default=2)
    regihour: int = Field(default=11)
    regiminute: int = Field(default=30)
    regisecond: int = Field(default=44735)
    teamahead: int = Field(default=6)
    customercnt: int = Field(default=2)
    customergroupcnt: int = Field(default=2)

class OutputModel(BaseModel):
    """response body"""
    predict: float = Field(
        600,
        description="wating time predict result"
        )


@router.post("/predict", response_model=OutputModel)
async def predict_wating_time(
    payload: InputModel,
    request: Request
    ) -> float:
    """predict waiting time router"""
    request_body = payload.__dict__
    trace_code = request.state.trace_code
    await logging("request", request_body, trace_code)
    # make input data   
    input_data = pd.DataFrame([request_body])
    # execute predict
    predict = MODEL.predict(
        input_data,
        num_iteration=MODEL.best_iteration
        )
    lambda_value = 0.3229772566823217
    prediction = inv_boxcox(predict[0], lambda_value)

    response_body = {"predict": prediction}
    await logging("response", response_body, trace_code)
    return response_body


async def logging(division: str, data: dict, trace_code: str) -> None:
    """logging json body"""
    data["trace_code"] = trace_code
    data["timestamp"] = str(datetime.now())
    LOGGER().info(
        f"{division}: {json.dumps(data, ensure_ascii=False)}"
        )
    data.pop("trace_code")
    data.pop("timestamp")
