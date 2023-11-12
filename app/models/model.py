from pydantic import BaseModel, Field, ValidationError, validator

class InputModel(BaseModel):
    """input parameter"""
    plantcode: str = Field(default='AL306')
    week_no: int = Field(default=36)
    waitingno: int = Field(default=73)
    week_int: int = Field(default=1)
    dayno: int = Field(default=7)
    daytype: int = Field(default=2)
    regitime: str = Field(default='10:06:32')
    teamahead: int = Field(default=6)
    customercnt: int = Field(default=2)
    customergroupcnt: int = Field(default=2)

    @validator('plantcode')
    def check_plantcode(cls, value):
        allowed_values = {'AL132', 'AL306', 'AL334', 'AL337', 'AL338'}
        if value not in allowed_values:
            raise ValueError(f"plantcode must be one of {', '.join(allowed_values)}")
        return value

    @validator('regitime')
    def validate_time_format(cls, value):
        if not cls.is_valid_time_format(value):
            raise ValueError("Invalid time format. Use 'HH:MM:SS' format.")
        return value

    @classmethod
    def is_valid_time_format(cls, value):
        try:
            parts = value.split(':')
            if len(parts) != 3:
                return False
            hours, minutes, seconds = map(int, parts)
            return 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60
        except (ValueError, IndexError):
            return False

class OutputModel(BaseModel):
    """response body"""
    predict: int = Field(
        600,
        description="wating time predict result"
        )