#!/bin/env bash

# configuration
MYSQL_ROOT_PASSWORD="root#pass123"
MYSQL_QUERYINFO_DBNAME="QueryInfo"
MYSQL_QUERYINFO_USER="QueryInfo"
MYSQL_QUERYINFO_PASSWORD="QueryInfo123"

# install mysql
echo "[+] Install mysql........................................................"
apt-get install -y mariadb-server mariadb-client
service mysql start
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE DATABASE ${MYSQL_QUERYINFO_DBNAME};GRANT ALL PRIVILEGES ON ${MYSQL_QUERYINFO_DBNAME}.* TO '${MYSQL_QUERYINFO_USER}'@'%' IDENTIFIED BY '${MYSQL_QUERYINFO_PASSWORD}';FLUSH PRIVILEGES;"
mysqld_safe

# config pip
echo "[+] Config pip..........................................................."
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# install package
echo "[+] Install package......................................................"
pip install -r requirements.txt

# Init db
echo "[+] Init db.............................................................."
flask db init
flask db migrate
flask db upgrade
