from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router as employee_router

app = FastAPI(
    title="Employee Management API",
    description="A RESTful API for managing employees protected by API Key authentication.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for local testing / frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router)


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Welcome to the Employee Management API",
        "documentation": "/docs",
        "authentication": "Pass 'X-API-Key' in headers for protected endpoints",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
