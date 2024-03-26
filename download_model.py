from datetime import datetime

from utils.s3_connector import s3Connector
from utils.slack_alert import EATSSlackNotice

slack = EATSSlackNotice('eats')

FILE_PATH = 'models'
S3_PATH = 'work/eats/forecast_waittime/model'
FILE_NAME_LIST = [
    'LGBM_V2.0.pkl',
    'lambda_value.txt',
    'plantcode_mapping.yaml'
]

for FILE_NAME in FILE_NAME_LIST:
    s3Connector.download_file(
        file_path=FILE_PATH,
        s3_path=S3_PATH,
        file_name=FILE_NAME,
    )

today = datetime.today().strftime('%Y-%m-%d')
slack.send_message(f"{today} 예측모델 다운로드 완료_태블릿")