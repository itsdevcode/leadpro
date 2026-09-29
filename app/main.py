from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.users import router as user_router
from app.api.v1.leads import router as lead_router
from app.api.v1.lead_comments import router as lead_comment_router
from app.core.redis import redis_client, check_redis_connection
from app.middleware.rate_limit import RateLimitMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_connected = await check_redis_connection()

    if not redis_connected:
        raise RuntimeError("Redis connection failed")

    yield

    await redis_client.aclose()


app = FastAPI(
    title="LeadPro AI",
    description="AI-powered lead generation and management platform",
    version="0.0.1",
    lifespan=lifespan,
)

app.add_middleware(
    RateLimitMiddleware,
    redis_client=redis_client,
    limit=5,
    window_seconds=60,
)

app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(lead_router, prefix="/api/v1/leads", tags=["leads"])
app.include_router(
    lead_comment_router,
    prefix="/api/v1/leads/comments",
    tags=["comments"],
)


@app.get("/health")
def healthcheck():
    return {"status": "ok"}