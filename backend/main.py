from fastapi import FastAPI
from google.cloud import bigquery
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# Permitir frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego puedes restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-excel")
def upload_excel(payload: dict):

    recetas = payload.get("recetas", [])
    nutrientes = payload.get("nutrientes", [])

    client = bigquery.Client()

    now = datetime.utcnow().isoformat()

    # Agregar timestamp
    for r in recetas:
        r["fecha_carga"] = now

    for n in nutrientes:
        n["fecha_carga"] = now

    if recetas:
        client.insert_rows_json(
            "TU_PROYECTO.TU_DATASET.recetas",
            recetas
        )

    if nutrientes:
        client.insert_rows_json(
            "TU_PROYECTO.TU_DATASET.nutrientes",
            nutrientes
        )

    return {"status": "ok"}
