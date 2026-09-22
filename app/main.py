from fastapi import FastAPI

app = FastAPI(
    title="LeadPro AI",
    description="AI-powered lead generation and management platform",
    version="0.0.1",
)


@app.get("/health")
def healthcheck():
    return {"status": "ok"}