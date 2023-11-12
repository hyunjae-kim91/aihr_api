from typing import Tuple
import pandas as pd
from scipy.special import inv_boxcox
import asyncio

async def transform_dataframe(request_body: dict) -> pd.DataFrame():
    request_body['plantcode_L'] = transform_plantcode(request_body['plantcode'])
    request_body['regihour'], request_body['regiminute'], request_body['regisecond'] = transform_time(request_body['regitime'])

    keys_to_remove = ['regitime', 'plantcode']
    for key in keys_to_remove:
        del request_body[key]
    print(request_body)
    
    column_order = ['plantcode_L', 'week_no', 'waitingno', 'week_int', 'dayno', 'daytype', 'regihour', 'regiminute', 'regisecond', 'teamahead', 'customercnt', 'customergroupcnt']
    return pd.DataFrame([request_body], columns=column_order)

async def transform_boxcox(predict: int) -> int:
    lambda_value = 0.3229772566823217
    predict_boxcox = inv_boxcox(predict[0], lambda_value)
    prediction = int(predict_boxcox)
    return prediction
    
def transform_plantcode(plantcode: str) -> int:
    plantcode_mapping = {
        'AL132': 0, 
        'AL306': 1, 
        'AL334': 2,
        'AL337': 3,
        'AL338': 4
    }
    return plantcode_mapping.get(plantcode, -1)
    
def transform_time(time_str: str) -> Tuple[int, int, int]:
    hour, minute, second = map(int, time_str.split(':'))
    regihour = hour
    regiminute = minute * 60 + second
    regisecond = hour * 3600 + minute * 60 + second
    return regihour, regiminute, regisecond