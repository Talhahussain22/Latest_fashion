from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import json
import os

app = FastAPI()

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("favicon.ico")

@app.get("/all_products")
async def get_latest_trends():
    try:
        if not os.path.exists("latest_batch.json"):
            raise HTTPException(status_code=404, detail="latest_batch.json not found")
        
        with open("latest_batch.json", "r") as f:
            data = json.load(f)
        
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Welcome to the Latest Fashion Trends API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
