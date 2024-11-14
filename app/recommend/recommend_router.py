import json
import joblib
from datetime import datetime
import numpy as np
from fastapi import APIRouter, Request

from app.models.model import InputModel, OutputModel, EmployeeDetailModel
from app.utils.logger_utils import Logger

router = APIRouter()
LOGGER = Logger()

@router.post("/recommend", response_model=OutputModel)
async def recommend_waiting_time(
    payload: InputModel,
    request: Request
):
    request_body = payload.dict()
    trace_code = request.state.trace_code
    await logging("request", request_body, trace_code)

    # JSON 파일에서 resultData 불러오기
    with open("recommend_test_data.json", "r", encoding="utf-8") as file:
        employee_data = json.load(file)

    # OutputModel 형식으로 응답 생성
    response_body = OutputModel(
        resultFlag=True,
        resultData=[EmployeeDetailModel(**data) for data in employee_data],
        errCode=None,
        errMessage=None
    )

    await logging("response", response_body.dict(), trace_code)
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