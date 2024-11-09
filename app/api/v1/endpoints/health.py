from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health check"])


# Health Check
@router.get("/")
async def check_health():
    return {"status": "System Healthy"}

