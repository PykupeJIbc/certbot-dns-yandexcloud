YandexCloud DNS Authenticator plugin for Certbot
================================================

Installation
------------
    pip install -e certbot-dns-yandexcloud/

Credentials
-----------
    dns_yandexcloud_sa_json_path = "./sa.json"
    dns_yandexcloud_folder_id = "b0g0kfc0jutlhm000r00"

Examples
--------
    certbot certonly \
    --authenticator dns-yandexcloud \
    --dns-yandexcloud-credentials ~/.secrets/certbot/yandexcloud.ini \
    --non-interactive --agree-tos --email username@example.com \
    -d 'example.com'