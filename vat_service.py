import requests
from vies_client import VIESClient


class VATCheckService:

    def __init__(self):
        self.vies = VIESClient()

    # 🟢 FIRMA → SUCHE (OpenCorporates)
    def search_company(self, name, address=""):

        query = name
        if address:
            query += " " + address

        url = f"https://api.opencorporates.com/v0.4/companies/search?q={query}"

        try:
            r = requests.get(url, timeout=10)
            data = r.json()

            companies = data.get("results", {}).get("companies", [])

            if not companies:
                return {"name": "", "address": "", "vat": ""}

            best = companies[0]["company"]

            return {
                "name": best.get("name", ""),
                "address": best.get("registered_address", ""),
                "vat": best.get("company_number", "")
            }

        except Exception:
            return {"name": "", "address": "", "vat": ""}

    # 🔵 USt-ID CHECK (VIES)
    def check_vat(self, vat: str):

        vat = vat.strip().replace(" ", "").upper()

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

        except Exception:
            return {
                "input": vat,
                "valid": False,
                "name": "",
                "address": "",
                "vat": ""
            }

    # 🟣 HAUPTFUNKTION (Firma → Daten suchen)
    def check_company(self, input_text: str):

        input_text = input_text.strip()

        result = self.search_company(input_text)

        return {
            "input": input_text,
            "valid": False,
            "name": result.get("name", ""),
            "address": result.get("address", ""),
            "vat": result.get("vat", "")
        }
