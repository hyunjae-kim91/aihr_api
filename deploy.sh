#!/bin/bash

CONFIG_PATH="./nginx/aihr_api.conf"
NGINX_CONTAINER="nginx"
EXIST_BLUE=$(docker-compose ps | grep aihr_api-blue)
EXIST_GREEN=$(docker-compose ps | grep aihr_api-green)

ensure_nginx_running() {
    if ! docker ps | grep -q "$NGINX_CONTAINER"; then
        echo "Nginx container is not running. Starting Nginx..."
        
        # nginx 빌드 추가
        docker-compose build nginx || { echo "Failed to build Nginx container"; exit 1; }
        
        # 먼저 nginx와 네트워크를 함께 실행하여 연결을 보장
        docker-compose up -d nginx || { echo "Failed to start Nginx container"; exit 1; }
        
        # Nginx가 정상적으로 연결되었는지 확인
        if ! docker inspect --format '{{.State.Running}}' "$NGINX_CONTAINER" | grep -q "true"; then
            echo "Nginx container failed to start correctly.";
            exit 1;
        fi
    fi
}

# Blue 또는 Green 배포 절차
deploy_instance() {
    if [ -z "$EXIST_BLUE" ] && [ -z "$EXIST_GREEN" ]; then
        # 두 인스턴스가 모두 꺼져 있을 때
        echo "Both Blue and Green instances are down. Deploying both..."
        docker-compose build aihr_api-blue || { echo "Failed to build aihr_api-blue"; exit 1; }
        docker-compose up -d aihr_api-blue || { echo "Failed to start aihr_api-blue"; exit 1; }
        
        docker-compose build aihr_api-green || { echo "Failed to build aihr_api-green"; exit 1; }
        docker-compose up -d aihr_api-green || { echo "Failed to start aihr_api-green"; exit 1; }

        # Nginx 작업 진행
        ensure_nginx_running
        
        # 하나를 내린다 (예시로 Blue 내리기)
        echo "Stopping Blue instance..."
        docker-compose down aihr_api-blue || { echo "Failed to bring down aihr_api-blue"; exit 1; }

    elif [ -z "$EXIST_BLUE" ]; then
        # Blue만 꺼져 있을 때
        echo "Deploying Blue instance..."
        docker-compose build aihr_api-blue || { echo "Failed to build aihr_api-blue"; exit 1; }
        docker-compose up -d aihr_api-blue || { echo "Failed to start aihr_api-blue"; exit 1; }

        # Nginx 작업 진행
        ensure_nginx_running
        
        # Green 인스턴스를 내린다
        echo "Stopping Green instance..."
        docker-compose down aihr_api-green || { echo "Failed to bring down aihr_api-green"; exit 1; }

    elif [ -z "$EXIST_GREEN" ]; then
        # Green만 꺼져 있을 때
        echo "Deploying Green instance..."
        docker-compose build aihr_api-green || { echo "Failed to build aihr_api-green"; exit 1; }
        docker-compose up -d aihr_api-green || { echo "Failed to start aihr_api-green"; exit 1; }

        # Nginx 작업 진행
        ensure_nginx_running
        
        # Blue 인스턴스를 내린다
        echo "Stopping Blue instance..."
        docker-compose down aihr_api-blue || { echo "Failed to bring down aihr_api-blue"; exit 1; }
    fi
}

# 불필요한 이미지 제거
cleanup_docker_images() {
    echo "Cleaning up unused Docker images..."
    docker image prune -f || { echo "Failed to prune images"; exit 1; }
    unused_images=$(docker images -f "dangling=true" -q)
    if [ ! -z "$unused_images" ]; then
        docker rmi $unused_images || echo "Failed to remove some unused images."
    fi
}

# 배포 실행 순서
deploy_instance    # Blue 또는 Green 배포
cleanup_docker_images

echo "Deployment completed successfully."
