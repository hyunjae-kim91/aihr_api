from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional

class InputModel(BaseModel):
    """input parameter"""
    input_prompt: str = Field(..., description="질의문")
    input_user: str = Field(..., description="사용자명")
    pernr: List[str] = Field(..., description="사번 리스트")

    # 기본 검증 로직: input_prompt와 input_user는 필수
    @validator("input_prompt", "input_user")
    def check_required_fields(cls, value):
        if not value:
            raise ValueError("필수 필드를 입력하세요.")
        return value

class EmployeeDetailModel(BaseModel):
    """직원 세부 정보"""
    employee_id: str
    employee_name: str
    position_level: str
    position_duration: float
    job_title: str
    department: str
    job_type: str
    employee_age: int
    employee_gender: str
    talent_type_ai: List[str]
    talent_type_profile: List[str]
    supporting_statement: str

class OutputModel(BaseModel):
    resultFlag: bool = Field(..., description="처리 성공 여부")
    resultData: Optional[List[EmployeeDetailModel]] = Field(default=[], description="결과 데이터")
    errCode: Optional[str] = None
    errMessage: Optional[str] = None
