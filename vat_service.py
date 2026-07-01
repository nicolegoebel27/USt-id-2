from vies_client import VIESClient
from bzst_client import BZStClient
from cache import VATCache
from circuit_breaker import CircuitBreaker
import time


class VATCheckService:

    def __init__(self):
        self.vies = VIESClient()
        self.bzst = BZStClient()
        self.cache = VATCache()
        self.cb = CircuitBreaker()

    def check(self, vat: str):

        vat = vat.replace(" ", "").upper()

        cached = self.cache.get(vat)
        if cached:
            cached["cached"] = True
            return cached

        if vat.startswith("DE"):
            try:
                result = self.bzst.check(vat)
                result["source"] = "BZSt"
                self.cache.set(vat, result)
                return result
            except Exception as e:
                return {"valid": False, "error": str(e)}

        country = vat[:2]
        number = vat[2:]

        try:
            result = self.vies.check(country, number)
            result["source"] = "VIES"
        except Exception as e:
            result = {"valid": False, "error": str(e), "source": "VIES"}

        self.cache.set(vat, result)
        return result