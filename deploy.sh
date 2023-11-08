# !/bin/sh
EXIST_BLUE=$(sudo docker-compose -f docker-compose-blue.yml ps | grep blue)
if [ -z "$EXIST_BLUE" ]; then
    echo "blue up"
    sudo docker-compose -f docker-compose-blue.yml build --no-cache
    sudo docker-compose -f docker-compose-blue.yml up -d
    sed -i 's/8002/8001/g' waiting_time.conf
    sudo docker cp waiting_time.conf nginx:/etc/nginx/conf.d/
    sudo docker exec -ti nginx-container /bin/bash -c 'service nginx reload'
    sleep 10
    sudo docker-compose -f docker-compose-green.yml down
else
    echo "green up"
    sudo docker-compose -f docker-compose-green.yml build --no-cache
    sudo docker-compose -f docker-compose-green.yml up -d
    sed -i 's/8001/8002/g' waiting_time.conf
    sudo docker cp waiting_time.conf nginx:/etc/nginx/conf.d/
    sudo docker exec -ti nginx-container /bin/bash -c 'service nginx reload'
    sleep 10
    sudo docker-compose -f docker-compose-blue.yml down
fi
