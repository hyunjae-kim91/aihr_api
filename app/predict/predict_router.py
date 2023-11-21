import json
import joblib
from datetime import datetime
import numpy as np
from fastapi import APIRouter, Request

from app.models.model import InputModel, OutputModel
from app.utils.logger_utils import Logger
from app.utils.transform_data import transform_boxcox, transform_dataframe

router = APIRouter()
MODEL = joblib.load('models/LGBM_v1.1.pkl')
LOGGER = Logger()

@router.post("/predict", response_model=OutputModel)
async def predict_wating_time(
    payload: InputModel,
    request: Request
    ) -> float:
    request_body = payload.__dict__
    trace_code = request.state.trace_code
    await logging("request", request_body, trace_code)
    input_data = await transform_dataframe(request_body)
    predict = MODEL.predict(
        input_data,
        num_iteration=MODEL.best_iteration
        )
    prediction = await transform_boxcox(predict)
    response_body = {
        "resultFlag": True,
        "resultData": prediction,
        "errCode": 'null',
        "errMessage": 'null'
    }
    
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