import json
import joblib
from datetime import datetime
import numpy as np
from fastapi import APIRouter, Request

from app.models.model import RecommendInputModel, EmployeeDetailModel, RecommendResultDataModel, RecommendOutputModel
from app.models.model import InfotypeOutputModel, InfotypeInputModel, InfotypeOutputDetailModel, HashtagKeywordsModel, HashtagModel
from app.utils.logger_utils import Logger
from db.db_function import execute_all_sql, get_query

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

    with open("src/recommend_test_data.json", "r", encoding="utf-8") as file:
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
    with open("src/infotype_test_data.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)

    info_type = json_data.get('resultData').get('infotype')
    
    return InfotypeOutputModel(
        resultFlag=True,
        resultData=InfotypeOutputDetailModel(
            empno=info_type["empno"],
            smry_st=info_type["smry_st"],
            tltp_ai=info_type["tltp_ai"],
            tltp_prof=info_type["tltp_prof"],
            tltp_htag_list=[HashtagKeywordsModel(
                tltp=info_type["tltp"],
                htag_list=[HashtagModel(
                    htag=hashtag["htag"],
                    bss_st=hashtag["bss_st"]
                ) for hashtag in info_type["htag_list"]]
            ) for info_type in info_type["tltp_htag_list"]]
        ),
        errCode=None,
        errMessage=None
    )

@router.post("/test")
async def get_test(
    request: Request
):
    query = get_query(SQL_PATH='sql',SQL_FILE='test.sql')
    test_data = execute_all_sql(query)
    return {
        'Result' : dict(test_data)
    }

async def logging(division: str, data: dict, trace_code: str) -> None:
    """logging json body"""
    data["trace_code"] = trace_code
    data["timestamp"] = str(datetime.now())
    LOGGER().info(
        f"{division}: {json.dumps(data, ensure_ascii=False)}"
        )
    data.pop("trace_code")
    data.pop("timestamp")