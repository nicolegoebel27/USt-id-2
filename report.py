from openpyxl import Workbook
ws.append(["Input", "Company", "Address", "VAT"])

class ExcelReport:

    def generate(self, data, file):

        wb = Workbook()
        ws = wb.active

        ws.append(["VAT", "Valid", "Source", "Cached", "Error"])

        for r in data:
           ws.append([
    r.get("input"),
    r.get("name"),
    r.get("address"),
    r.get("vat")
])

        wb.save(file)
