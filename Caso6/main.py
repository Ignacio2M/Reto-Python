import uvicorn
from fastapi import FastAPI, HTTPException
from db import DB

app = FastAPI()
db = DB('../Caso5.txt')

@app.get("/{matricula}")
async def read_matricula(matricula: str):
    try:
        data = db.getMatricula(matricula)
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@app.get("/healthcheck/")
def healthcheck():
    return {"ok": 1}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")