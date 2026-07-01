from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse

from vat_service import VATCheckService
from report import ExcelReport

app = FastAPI()

service = VATCheckService()
report = ExcelReport()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>USt-IdNr Checker</h2>

    <form action="/upload" enctype="multipart/form-data" method="post">
        <input type="file" name="file">
        <button type="submit">Prüfen</button>
    </form>
    """


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    content = await file.read()
    lines = content.decode().splitlines()

    results = []

    for vat in lines:
        vat = vat.strip()
        if not vat:
            continue

        result = service.check(vat)

        results.append({
            "vat": vat,
            "valid": result.get("valid"),
            "source": result.get("source"),
            "cached": result.get("cached"),
            "error": result.get("error", "")
        })

    output_file = "output.xlsx"
    report.generate(results, output_file)

    return FileResponse(output_file, filename="UStId_Report.xlsx")