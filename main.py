from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import requests

# Deep AI
api_key         = ""

# Sightengine
api_user        = ""
api_secret      = ""

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/moderate_sightengine/")
async def sightengine_moderate(file: UploadFile = File(...)):

    # Проверка типа файла
    if not file.content_type.startswith("image/"):
        return JSONResponse(status_code=400, content={"error": "Файл должен быть изображением"})

    image_data = await file.read()

    params = {
        'models': 'nudity-2.1',
        'api_user': api_user,
        'api_secret': api_secret
    }

    response = requests.post(
        'https://api.sightengine.com/1.0/check.json',
        files={'media': (file.filename, image_data, file.content_type)},
        data = params
    )

    if response.status_code != 200:
        return JSONResponse(status_code=response.status_code, content={"error": "Ошибка от Sightengine", "details": response.text})

    result = response.json()

    nudity = result.get("nudity", {})
    thresholds = {
        "sexual_activity": 0.2,
        "sexual_display": 0.2,
        "erotica": 0.25,
        "very_suggestive": 0.4,
        "suggestive": 0.5,
        "mildly_suggestive": 0.6,
    }

    for key, threshold in thresholds.items():
        if nudity.get(key, 0) > threshold:
            return {"status": "REJECTED", "reason": f"Detected {key} ({nudity[key]:.3f})"}

    return {"status": "OK"}

@app.post("/moderate_deepai/")
async def deepai_moderate(file: UploadFile = File(...)):
    
    if not file.content_type.startswith("image/"):
        return JSONResponse(status_code=400, content={"error": "Файл должен быть изображением"})

    
    image_data = await file.read()

    response = requests.post(
        'https://api.deepai.org/api/nsfw-detector',
        headers={'api-key': api_key},
        files={'image': (file.filename, image_data, file.content_type)}
    )

    if response.status_code != 200:
        return JSONResponse(status_code=response.status_code, content={"error": "Ошибка от DeepAI", "details": response.text})

    result = response.json()

    nsfw_score = result.get("output", {}).get("nsfw_score", 0)

    if nsfw_score > 0.7:
        return {
            "status": "REJECTED", "reason": "NSFW content"
        }
    else:
        return{
            "status": "OK"
        }