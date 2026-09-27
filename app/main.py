from fastapi import FastAPI
from app.api.v1.users import router as user_router
from app.api.v1.leads import router as lead_router

app = FastAPI(
    title="LeadPro AI",
    description="AI-powered lead generation and management platform",
    version="0.0.1",
)

app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(lead_router, prefix="/api/v1/leads", tags=["leads"])

@app.get("/health")
def healthcheck():
    return {"status": "ok"}