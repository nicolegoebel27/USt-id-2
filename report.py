from openpyxl import Workbook


class ExcelReport:

    def generate(self, data, file):

        wb = Workbook()
        ws = wb.active   

        ws.append(["Input", "Company", "Address", "VAT"])

        for r in data:
            ws.append([
                r.get("input", ""),
                r.get("name", ""),
                r.get("address", ""),
                r.get("vat", "")
            ])

        wb.save(file)
