# Quick installation (Debian 8)

## Install components
* apt-get update
* apt-get install python-pip python-dev nginx
* pip install virtualenv

## Create a Python virtualenv
* mkdir -p /var/www/curldu.mp
* cd /var/www/curldu.mp/
* virtualenv curldump
* source curldump/bin/activate

## Setup dependencies
* pip install uwsgi flask python-magic
* deactivate

## Setup curldump
* copy curldump.py to /var/www/curldu.mp
* mkdir /var/www/curldu.mp/files
* echo "CREATE TABLE short(s TEXT, h TEXT, dt DATETIME);" | sqlite3 /var/www/curldu.mp/short.db
* chown -R www-data /var/www/curldu.mp

## Configure Nginx + uwsgi
* vi /etc/nginx/site-available/curldu.mp :
```
server {
    listen [::]:80 ipv6only=on;
    server_name curldu.mp;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/curldu.mp/curldump.sock;
    }
}
```
* vi /var/www/curldu.mp/wsgi.py :
```
from curldump import application

if __name__ == "__main__":
    application.run()
```
* vi /var/www/curldu.mp/curldump.ini
```
[uwsgi]
module = wsgi

master = true
processes = 5

socket = curldump.sock
chmod-socket = 660
chown-socket = www-data
vacuum = true

die-on-term = true
```
* vi /etc/init.d/curldump
```
case "$1" in
    start)
        export PATH=/var/www/curldu.mp/curldump/bin
        cd /var/www/curldu.mp
        exec uwsgi --ini curldump.ini &
        ;;
    stop)
        pkill uwsgi
        ;;
esac
```
* ln -s /etc/nginx/sites-available/curldu.mp /etc/nginx/sites-enabled
* chmod +x /etc/init.d/curldump
* service nginx restart
* /etc/init.d/curldump start
