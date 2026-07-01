from vies_client import VIESClient
from bzst_client import BZStClient
from cache import VATCache
from circuit_breaker import CircuitBreaker
import time

def clean_vat(vat: str):
    return (
        vat.strip()
        .replace(" ", "")
        .replace("\n", "")
        .replace("\r", "")
        .upper()
    )


class VATCheckService:

    def search_company(self, name, address=""):

    query = name
    if address:
        query += " " + address

    url = f"https://api.opencorporates.com/v0.4/companies/search?q={query}"

    try:
        import requests
        r = requests.get(url, timeout=10)
        data = r.json()

        companies = data.get("results", {}).get("companies", [])

        if not companies:
            return {"name": "", "vat": "", "address": ""}

        best = companies[0]["company"]

        return {
            "name": best.get("name", ""),
            "address": best.get("registered_address", ""),
            "vat": best.get("company_number", "")
        }

    except Exception as e:
        return {"name": "", "vat": "", "address": "", "error": str(e)}



    def __init__(self):
        self.vies = VIESClient()
        self.bzst = BZStClient()
        self.cache = VATCache()
        self.cb = CircuitBreaker()

    def check(self, input_text: str, mode="company"):

    input_text = input_text.strip()

    # 🔵 MODE 1: USt-ID Prüfung (optional weiter nutzbar)
    if mode == "vat":

        vat = input_text.replace(" ", "").upper()
        country = vat[:2]
        number = vat[2:]

        try:
            result = self.vies.check(country, number)
            return {
                "input": vat,
                "valid": result.get("valid", False),
                "name": result.get("name", ""),
                "address": result.get("address", ""),
                "vat": vat
            }
        except:
            return {
                "input": vat,
                "valid": False,
                "name": "",
                "address": "",
                "vat": ""
            }

    # 🟢 MODE 2: FIRMA → USt-ID Suche
    result = self.search_company(input_text)

    return {
        "input": input_text,
        "valid": False,
        "name": result.get("name", ""),
        "address": result.get("address", ""),
        "vat": result.get("vat", "")
    }

country = vat[:2]
number = vat[2:]

        try:
            result = self.vies.check(country, number)
            result["source"] = "VIES"
        except Exception as e:
            result = {"valid": False, "error": str(e), "source": "VIES"}

        self.cache.set(vat, result)
        return result
