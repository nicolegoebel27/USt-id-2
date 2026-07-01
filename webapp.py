from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uvicorn

from vat_service import VATCheckService
from report import ExcelReport

app = FastAPI()

service = VATCheckService()
report = ExcelReport()


# 🧠 automatische Erkennung
def is_vat(text: str):
    text = text.strip().replace(" ", "").upper()
    return len(text) > 6 and text[:2].isalpha() and any(c.isdigit() for c in text)


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    content = await file.read()

    # robust decode (Excel / Windows / UTF-8)
    try:
        text = content.decode("utf-8")
    except:
        text = content.decode("latin-1")

    lines = text.splitlines()

    results = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        try:
            # 🔵 USt-ID Modus
            if is_vat(line):
                result = service.check_vat(line)

            # 🟢 Firmenname Modus
            else:
                result = service.check_company(line)

        except Exception as e:
            result = {
                "input": line,
                "valid": False,
                "name": "",
                "address": "",
                "vat": "",
                "error": str(e)
            }

        results.append(result)

    # 📊 Excel erstellen
    output_file = "output.xlsx"
    report.generate(results, output_file)

    return FileResponse(
        output_file,
        filename="USt_Report.xlsx"
    )


# 🔥 optional für lokalen Start
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
