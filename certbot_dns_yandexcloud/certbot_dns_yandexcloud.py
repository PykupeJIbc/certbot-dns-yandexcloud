"""DNS Authenticator for YandexCloud."""
import logging
from typing import Any
from typing import Callable
from typing import Optional

import yandexcloud
from yandex.cloud.dns.v1.dns_zone_service_pb2_grpc import DnsZoneServiceStub
from yandex.cloud.dns.v1.dns_zone_service_pb2 import ListDnsZonesRequest
from yandex.cloud.dns.v1.dns_zone_service_pb2 import UpsertRecordSetsRequest
from yandex.cloud.dns.v1.dns_zone_pb2 import RecordSet

import grpc
import json
from google.protobuf.json_format import MessageToJson

from certbot import errors
from certbot.plugins import dns_common
from certbot.plugins.dns_common import CredentialsConfiguration

logger = logging.getLogger(__name__)


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for YandexCloud

    This Authenticator uses the YandexCloud API to fulfill a dns-01 challenge.
    """

    description = 'Obtain certificates using a DNS TXT record (if you are ' + \
                  'using YandexCloud for DNS).'
    ttl = 600

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.credentials: Optional[CredentialsConfiguration] = None

    @classmethod
    def add_parser_arguments(cls, add: Callable[..., None],
                             default_propagation_seconds: int = 10) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add('credentials', help='YandexCloud credentials INI file.')

    def more_info(self) -> str:
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the YandexCloud API.'

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            'credentials',
            'YandexCloud credentials INI file',
            {
                'sa_json_path': 'YandexCloud service account json path',
                'folder_id': 'YandexCloud folder ID'
            }
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_yandexcloud_client().add_txt_record(
            self.credentials.conf('folder_id'), domain, validation_name, validation, self.ttl
        )

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_yandexcloud_client().del_txt_record(
            self.credentials.conf('folder_id'), domain, validation_name, validation, self.ttl
        )

    def _get_yandexcloud_client(self) -> "_YandexCloudClient":
        if not self.credentials:  # pragma: no cover
            raise errors.Error("Plugin has not been prepared.")
        return _YandexCloudClient(self.credentials.conf('sa_json_path'))



class _YandexCloudClient():
    """
    Encapsulates all communication with the YandexCloud API.
    """
    def __init__(self, sa_json_path: str) -> None:
        interceptor = yandexcloud.RetryInterceptor(max_retry_count=5, retriable_codes=[grpc.StatusCode.UNAVAILABLE])
        
        with open(sa_json_path) as infile:
            self.sdk = yandexcloud.SDK(interceptor=interceptor, service_account_key=json.load(infile))

    def add_txt_record(self, folder_id, domain: str, record_name: str, recodr_content: str, record_ttl: int) -> None:
        zone_id = self._find_zone_id(folder_id, domain)

        self.sdk.client(DnsZoneServiceStub).UpsertRecordSets(
            UpsertRecordSetsRequest(
                dns_zone_id=zone_id, merges=[RecordSet(
                    name=f"{record_name}.", type="TXT", ttl=record_ttl, data=[recodr_content]
                )]
            )
        )

        logger.debug('Successfully added TXT record with id: %s', record_name)

    def del_txt_record(self, folder_id, domain: str, record_name: str, recodr_content: str, record_ttl: int) -> None:
        zone_id = self._find_zone_id(folder_id, domain)

        self.sdk.client(DnsZoneServiceStub).UpsertRecordSets(
            UpsertRecordSetsRequest(
                dns_zone_id=zone_id, deletions=[RecordSet(
                    name=f"{record_name}.", type="TXT", ttl=record_ttl, data=[recodr_content]
                )]
            )
        )

        logger.debug('Removing TXT record with id: %s', record_name)

    def _find_zone_id(self,folder_id: str, domain: str) -> str:

        domain_name_guesses = dns_common.base_domain_name_guesses(domain)

        zones = json.loads(MessageToJson(
            self.sdk.client(DnsZoneServiceStub).List(ListDnsZonesRequest(
                folder_id=folder_id
            ))
        ))

        for guess in domain_name_guesses:
            matches = [zone for zone in zones['dnsZones'] if zone['zone'] == f"{guess}."]
            if matches:
                zone_id = matches[0]['id']
                logger.debug('Found zone id for %s using name %s', domain, guess)
                return zone_id

        raise errors.PluginError(f'Unable to determine zone id for {domain} using names: '
                                 f'{domain_name_guesses}.')
