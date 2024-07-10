import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI, HTTPException

uri = "mongodb://root:example@localhost:27017/"
client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
db = client.get_database("cars")
cars_collection = db.get_collection("updates")

app = FastAPI()


@app.get("/{matricula}")
async def read_matricula(matricula: str):
    data = await cars_collection.find_one(
        {"Matricula": matricula}, {'Pos_date': 1}
    )
    if data is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return data['Pos_date']


@app.get("/healthcheck/")
async def healthcheck():
    return await client.admin.command('ping')


if __name__ == "__main__":
    uvicorn.run(app)
