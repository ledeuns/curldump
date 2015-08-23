server {
    listen [::]:80 ipv6only=on;
    server_name curldu.mp;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/curldu.mp/curldump.sock;
    }
}
