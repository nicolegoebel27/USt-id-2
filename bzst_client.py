class BZStClient:

    def check(self, vat):

        if not vat.startswith("DE"):
            return {"valid": False, "error": "not DE"}

        if len(vat) != 11:
            return {"valid": False, "error": "invalid length"}

        return {
            "valid": True,
            "vat": vat
        }