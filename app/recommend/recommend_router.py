import json
import joblib
from datetime import datetime
import numpy as np
from fastapi import APIRouter, Request

from app.models.model import RecommendInputModel, EmployeeDetailModel, RecommendResultDataModel, RecommendOutputModel
from app.models.model import InfotypeOutputModel, InfotypeInputModel, InfotypeOutputDetailModel, HashtagKeywordsModel, HashtagModel
from app.utils.logger_utils import Logger

router = APIRouter()
LOGGER = Logger()

@router.post("/recommend", response_model=RecommendOutputModel)
async def get_recommendation(
    payload: RecommendInputModel,
    request: Request
):
    request_body = payload.dict()
    trace_code = request.state.trace_code
    await logging("request", request_body, trace_code)

    with open("recommend_test_data.json", "r", encoding="utf-8") as file:
        employee_data = json.load(file)

    response_body = RecommendOutputModel(
        resultFlag=True,
        resultData=RecommendResultDataModel(
            response_prompt=employee_data["resultData"]["response_prompt"],
            recommendation=[
                EmployeeDetailModel(**recommend) 
                for recommend in employee_data["resultData"]["recommendation"]
            ],
        ),
        errCode=None,
        errMessage=None
    )

    await logging("response", response_body.dict(), trace_code)
    return response_body

@router.post("/infotype", response_model=InfotypeOutputModel)
async def get_infotype(
    payload: InfotypeInputModel,
    request: Request
):
    # JSON 파일에서 데이터 로드
    with open("infotype_test_data.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)

    response_data = json_data.get('resultData')
    
    return InfotypeOutputModel(
        resultFlag=True,
        resultData=InfotypeOutputDetailModel(
            employee_id=response_data["infotype"]["employee_id"],
            summarize=response_data["infotype"]["summarize"],
            talent_type_ai=response_data["infotype"]["talent_type_ai"],
            talent_type_profile=response_data["infotype"]["talent_type_profile"],
            hashtag_keywords=[HashtagKeywordsModel(
                talent_type_ai=info_type["talent_type_ai"],
                hashtag_list=[HashtagModel(
                    hashtag=hashtag["hashtag"],
                    supporting_sentence=hashtag["supporting_sentence"]
                ) for hashtag in info_type["hashtag_list"]]
            ) for info_type in response_data["infotype"]["hashtag_keywords"]]
        ),
        errCode=None,
        errMessage=None
    )
async def logging(division: str, data: dict, trace_code: str) -> None:
    """logging json body"""
    data["trace_code"] = trace_code
    data["timestamp"] = str(datetime.now())
    LOGGER().info(
        f"{division}: {json.dumps(data, ensure_ascii=False)}"
        )
    data.pop("trace_code")
    data.pop("timestamp")