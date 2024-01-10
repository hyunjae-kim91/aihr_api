FROM python:3.9

WORKDIR /app
# 소스 복사
COPY . .

# 시간 세팅 (KST 기준)
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# 크론 세팅 (모델 다운로드)
RUN apt-get update && apt-get install -y cron

COPY cronjob.sh /etc/cron.d/cronjob.sh
RUN chmod 777 /etc/cron.d/cronjob.sh
RUN crontab /etc/cron.d/cronjob.sh
CMD ["cron", "f"]

# python 라이브러리 설치
RUN pip3 install -r requirements.txt --no-cache-dir

# 로그 디렉토리 생성
RUN mkdir -p logs
RUN mkdir -p models

# run service
RUN chmod 777 run.sh
CMD bash run.sh