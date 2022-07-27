from setuptools import setup, find_packages

version = '0.0.1'

install_requires = [
    'yandexcloud>=0.175.0',
    'certbot>=1.29.0',
]

with open("README.md") as f:
    long_description = f.read()

setup(
    name='certbot-dns-yandexcloud',
    version=version,
    description='YandexCloud DNS Authenticator plugin for Certbot',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/PykupeJIbc/certbot-dns-yandexcloud',
    author='Timur Gusmanov',
    author_email='archrunel@gmail.com',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3 :: Only",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    
    packages=find_packages(),
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-yandexcloud = certbot_dns_yandexcloud.certbot_dns_yandexcloud:Authenticator',
        ],
    },
)