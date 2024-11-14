# !/bin/sh
CONFIG_PATH="./nginx/aihr_api.conf"
EXIST_BLUE=$(sudo docker-compose -f docker-compose-blue.yml ps | grep blue)

if [ ! -f "$CONFIG_PATH" ]; then
    echo "Error: Configuration file aihr_api.conf not found at $CONFIG_PATH"
    exit 1
fi

if [ -z "$EXIST_BLUE" ]; then
    echo "Blue deployment is up next."
    sudo docker-compose -f docker-compose-blue.yml build --no-cache
    sudo docker-compose -f docker-compose-blue.yml up -d
    sed -i 's/8002/8001/g' "$CONFIG_PATH"
    sudo docker cp "$CONFIG_PATH" nginx:/etc/nginx/conf.d/aihr_api.conf
    sudo docker exec -ti nginx /bin/bash -c 'service nginx reload'
    sleep 10
    sudo docker-compose -f docker-compose-green.yml down
else
    echo "Green deployment is up next."
    sudo docker-compose -f docker-compose-green.yml build --no-cache
    sudo docker-compose -f docker-compose-green.yml up -d
    sed -i 's/8001/8002/g' "$CONFIG_PATH"
    sudo docker cp "$CONFIG_PATH" nginx:/etc/nginx/conf.d/aihr_api.conf
    sudo docker exec -ti nginx /bin/bash -c 'service nginx reload'
    sleep 10
    sudo docker-compose -f docker-compose-blue.yml down
fi
