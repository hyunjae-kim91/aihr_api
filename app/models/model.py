from pydantic import BaseModel, Field, validator
from datetime import datetime

class CustomValidationException(Exception):
    def __init__(self, message: str):
        self.message = message

class InputModel(BaseModel):
    """input parameter"""
    plantcode: str = Field(default='AL132')
    waitingno: int = Field(default=10)
    daytype: int = Field(default=3)
    regidatetime: str = Field(default='2024-03-01 12:00:00')
    teamahead: int = Field(default=5)
    customercnt: int = Field(default=2)
    customergroupcnt: int = Field(default=2)

    @validator("regidatetime")
    def validate_regitime_format(cls, value):
        try:
            # 날짜 및 시간 형식이 맞는지 확인
            datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return value
        except ValueError:
            raise CustomValidationException("올바른 날짜 및 시간 형식이 아닙니다. 'yyyy-mm-dd hh:mm:ss' 형식을 사용하세요.")
    
    @validator("waitingno", "customercnt")
    def validate_waiting_customercnt(cls, value):
        if not isinstance(value, int) or value <= 0:
            raise CustomValidationException("1 이상 자연수를 입력하세요.")
        return value
    
    @validator("daytype")
    def validate_daytype(cls, value):
        if value not in (1, 2, 3):
            raise CustomValidationException("날짜 형식은 1, 2, 3 중 하나입니다.")
        return value

    @validator("teamahead")
    def validate_teamahead(cls, value):
        if not isinstance(value, int) or value < 0:
            raise CustomValidationException("내 앞 대기 팀 수는 0 또는 양수입니다.")
        return value

    @validator("customergroupcnt")
    def validate_customergroupcnt(cls, value):
        if value not in (2, 4, 6):
            raise CustomValidationException("고객 그룹 수는 2, 4, 6 중 하나입니다.")
        return value

class OutputModel(BaseModel):
    resultFlag : bool
    resultData: int = Field(default=0)
    errCode: str
    errMessage: str