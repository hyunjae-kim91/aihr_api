import os
from datetime import datetime

from utils.s3_connector import s3Connector
from utils.slack_alert import EATSSlackNotice

slack = EATSSlackNotice('eats')

s3Connector.download_file(
    file_path='models',
    file_name='LGBM_V2.0.pkl',
    s3_path='work/eats/forecast_waittime/model'
)
s3Connector.download_file(
    file_path='models',
    file_name='lambda_value.txt',
    s3_path='work/eats/forecast_waittime/model'
)

today = datetime.today().strftime('%Y-%m-%d')
slack.send_message(f"{today} 예측모델 다운로드 완료")