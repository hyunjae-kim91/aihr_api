from pydantic import BaseModel, Field, validator
from datetime import datetime

class CustomValidationException(Exception):
    def __init__(self, message: str):
        self.message = message

class InputModel(BaseModel):
    """input parameter"""
    plantcode: str = Field(default='AL306')
    waitingno: int = Field(default=1)
    daytype: int = Field(default=1)
    regidatetime: str = Field(default='2023-11-01 10:00:00')
    teamahead: int = Field(default=0)
    customercnt: int = Field(default=2)
    customergroupcnt: int = Field(default=2)

    @validator('plantcode')
    def check_plantcode(cls, value):
        allowed_values = {'AL132', 'AL306', 'AL334', 'AL337', 'AL338'}
        if value not in allowed_values:
            raise CustomValidationException(f"매장코드를 정확히 입력해주세요. {allowed_values}")
        return value

    @validator("regidatetime")
    def validate_regitime_format(cls, value):
        try:
            # 날짜 및 시간 형식이 맞는지 확인
            datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return value
        except ValueError:
            raise CustomValidationException("올바른 날짜 및 시간 형식이 아닙니다. 'yyyy-mm-dd hh:mm:ss' 형식을 사용하세요.")

class OutputModel(BaseModel):
    resultFlag : bool
    resultData: int = Field(default=0)
    errCode: str
    errMessage: str