레스토랑 대시시간 예측

Docker image 
1. sudo docker build -t predict:v1.x .
2. sudo docker images
3. sudo docker run -d -p 8000:8000 predict:v1.x

Local

1. pip install -r requirements.txt
2. bash run.sh
3. localhost:8000/docs 접속
