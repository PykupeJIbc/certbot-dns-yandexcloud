YandexCloud DNS Authenticator plugin for Certbot
================================================

[yandexcloud](https://cloud.yandex.ru/) DNS Authenticator plugin for [certbot](https://certbot.eff.org/).

This plugin automates the process of completing a dns-01 challenge by creating, and subsequently removing, TXT records using the yandexcloud [API](https://github.com/yandex-cloud/cloudapi)

Installation
------------
    pip install certbot-dns-yandexcloud

Certbot Arguments
---------------

To start using DNS authentication for yandexcloud, pass the following arguments on certbot's command line:

Option|Description|
---|---|
`--authenticator dns-yandexcloud`|select the authenticator plugin (Required)|
`--dns-yandexcloud-credentials FILE_PATH`|yandexcloud credentials INI file path. (Required)|

Credentials
-----------

Before credentials.ini providing create [yandexcloud service account](https://cloud.yandex.ru/docs/iam/operations/sa/create) and create [service-account-key](https://cloud.yandex.ru/docs/cli/operations/authentication/service-account) and get your folder_id where DNS zone is created

An example `credentials.ini` file:

``` {.sourceCode .ini}
    dns_yandexcloud_sa_json_path = "~/.secrets/certbot/sa.json"
    dns_yandexcloud_folder_id = "b0g0kfc0jutlhm000r00"
```

Examples
--------
    certbot certonly \
    --authenticator dns-yandexcloud \
    --dns-yandexcloud-credentials ~/.secrets/certbot/yandexcloud.ini \
    --non-interactive --agree-tos --email username@example.com \
    -d 'example.com'