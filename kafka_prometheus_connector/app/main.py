from fastapi import FastAPI, HTTPException
from app.routes import router

app = FastAPI(title="Kafka Connect Emulator", version="1.0")

# Register API routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Kafka Connect Emulator is running"}
