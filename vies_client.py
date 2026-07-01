from zeep import Client
from zeep.transports import Transport
import requests

WSDL = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"


class VIESClient:

    def __init__(self):
        session = requests.Session()
        transport = Transport(session=session, timeout=10)
        self.client = Client(wsdl=WSDL, transport=transport)

    def check(self, country, vat):
        response = self.client.service.checkVat(
            countryCode=country,
            vatNumber=vat
        )

        return {
            "valid": response.valid,
            "name": getattr(response, "name", None),
            "address": getattr(response, "address", None)
        }