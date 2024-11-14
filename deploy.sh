#!/bin/sh

CONFIG_PATH="./nginx/aihr_api.conf"
NGINX_CONTAINER="nginx-container"
EXIST_BLUE=$(sudo docker-compose -f docker-compose-blue.yml ps | grep aihr_api-blue)

# Health check 함수
health_check() {
    local port=$1
    local max_retries=10
    local retries=0

    until curl -sf "http://localhost:${port}" > /dev/null; do
        retries=$((retries + 1))
        if [ $retries -ge $max_retries ]; then
            echo "Health check failed on port ${port}"
            return 1
        fi
        sleep 3
    done
    echo "Health check passed on port ${port}"
    return 0
}

# 기존 blue/green 컨테이너가 있을 경우 강제 삭제
cleanup_container() {
    local container_name=$1
    if sudo docker ps -a --format '{{.Names}}' | grep -Eq "^${container_name}$"; then
        echo "Removing existing container: ${container_name}"
        sudo docker rm -f "${container_name}"
    fi
}

# Nginx 컨테이너가 실행 중인지 확인하고, 실행되지 않으면 실행
ensure_nginx_running() {
    if ! sudo docker ps --format '{{.Names}}' | grep -q "^${NGINX_CONTAINER}$"; then
        echo "Nginx container is not running. Starting nginx container..."
        sudo docker run -d --name "$NGINX_CONTAINER" -p 80:80 -v /path/to/nginx/config:/etc/nginx/conf.d nginx
        echo "Nginx container started."
    else
        echo "Nginx container is already running."
    fi
}

# Nginx 실행 확인
ensure_nginx_running

# Blue 또는 Green 배포
if [ -z "$EXIST_BLUE" ]; then
    echo "Starting Blue deployment."
    sudo docker-compose -f docker-compose-green.yml down  # 이전 green 컨테이너 종료
    cleanup_container "aihr_api-blue"  # 기존 blue 컨테이너 강제 삭제
    sudo docker-compose -f docker-compose-blue.yml up -d  # 새로운 blue 컨테이너 백그라운드 실행
else
    echo "Starting Green deployment."
    sudo docker-compose -f docker-compose-blue.yml down  # 이전 blue 컨테이너 종료
    cleanup_container "aihr_api-green"  # 기존 green 컨테이너 강제 삭제
    sudo docker-compose -f docker-compose-green.yml up -d  # 새로운 green 컨테이너 백그라운드 실행
fi

# Nginx 설정 복사 및 리로드
sudo docker cp "$CONFIG_PATH" "$NGINX_CONTAINER:/etc/nginx/conf.d/aihr_api.conf"
sudo docker exec -ti "$NGINX_CONTAINER" /bin/bash -c 'service nginx reload'

echo "Deployment completed successfully."
