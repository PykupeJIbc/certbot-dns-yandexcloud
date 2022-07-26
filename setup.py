from setuptools import setup, find_packages

setup(
    name='certbot-dns-yandexcloud',
    version='0.0.1',
    description='YandexCloud DNS Authenticator plugin for Certbot',
    package='certbot_dns_yandexcloud.py',
    install_requires=[
        'yandexcloud'
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'certbot.plugins': [
            'dns-yandexcloud = certbot_dns_yandexcloud:Authenticator',
        ],
    },
)