from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from core.config import config
from core.logs import logger
from .routes import v1_router

app = FastAPI(
    debug=config.debug,
    title=config.title,
    description=config.summary,
    version=config.version,
    openapi_url="/api/openapi.json",
    docs="/api/docs",
    contact={
        "name": config.author,
        "email": config.email,
    },
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(v1_router)

@app.on_event("startup")
def app_start():
    print("FastAPI app started_")
    logger.info("FastAPI app started")
    logger.info(config)

@app.on_event("shutdown")
def app_stop():
    print("FastAPI app stopped")

@app.get("/")
async def root():
    return {"message": "Welcome to OCR-LLM API"}