from openpyxl import Workbook


class ExcelReport:

    def generate(self, data, file):

        wb = Workbook()
        ws = wb.active

        ws.append(["VAT", "Valid", "Source", "Cached", "Error"])

        for r in data:
            ws.append([
                r.get("vat"),
                r.get("valid"),
                r.get("source"),
                r.get("cached"),
                r.get("error")
            ])

        wb.save(file)
