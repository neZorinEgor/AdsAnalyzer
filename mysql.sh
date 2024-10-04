sudo aa-remove-unknown
sudo systemctl restart snapd.apparmor
docker container prune
docker run --name mysql-container \
    -e MYSQL_HOST=127.0.0.1 \
    -e MYSQL_PORT=3306 \
    -e MYSQL_USER=user \
    -e MYSQL_DATABASE=database \
    -e MYSQL_PASSWORD=password \
    -e MYSQL_ROOT_PASSWORD=root_password \
    -p 3306:3306 \
    mysql:latest