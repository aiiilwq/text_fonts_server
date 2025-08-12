from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FONT_DIR = "fonts"
os.makedirs(FONT_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>✅ Сервер шрифтов работает</h1>
            <p>Доступные пути:</p>
            <ul style="list-style:none;">
                <li><b>GET</b> <a href="/fonts">/fonts</a> — список шрифтов</li>
                <li><a href="/docs">Документация API</a></li>
            </ul>
        </body>
    </html>
    """

@app.get("/fonts")
def list_fonts():
    files = [f for f in os.listdir(FONT_DIR) if f.lower().endswith((".ttf", ".otf"))]
    return {"fonts": files}

@app.post("/fonts")
def upload_font(file: UploadFile = File(...)):
    ALLOWED_EXTENSIONS = {".ttf", ".otf"}
    if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        return {"error": "Only .ttf and .otf files are allowed"}
    
    file_path = os.path.join(FONT_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"status": "ok", "filename": file.filename}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fonts/{filename}")
def get_font(filename: str):
    file_path = os.path.join(FONT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="font/ttf")
    return {"error": "Font not found"}, 404