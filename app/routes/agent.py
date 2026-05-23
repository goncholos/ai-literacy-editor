from fastapi import APIRouter
from app.models.schemas import AgentRequest
from app.services.agent_loop import run_agent

router = APIRouter(prefix="/agent")

@router.post("/run")
async def run(request: AgentRequest):
    return run_agent(request.task)