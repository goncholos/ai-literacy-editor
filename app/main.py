from fastapi import FastAPI
from app.routes.agent import router as agent_router

app = FastAPI(title="My First AI Agent")

app.include_router(agent_router)

@app.get("/health")
async def health():
    return {"status": "ok"}