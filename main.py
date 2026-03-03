from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io

app = FastAPI()

session = new_session(model_name="u2net", model_path="models/u2net.onnx")

@app.get("/")
def home():
    return {"message": "Background Remover API running"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    input_bytes = await file.read()

    output = remove(input_bytes, session=session)

    return StreamingResponse(
        io.BytesIO(output),
        media_type="image/png"
    )