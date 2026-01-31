from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from datetime import datetime

from app.core.config import settings
from app.routes import predict, feedback
from app.models.loader import ModelLoader

# Configure Logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Load ML models on startup.
    """
    logger.info("Application startup: Loading ML models...")
    loader = ModelLoader.get_instance()
    try:
        loader.load_model(settings.MODEL_PATH, settings.VECTORIZER_PATH)
        logger.info("ML models loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load ML models: {e}")
    
    yield
    
    logger.info("Application shutdown.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS code
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")
templates_dir = os.path.join(base_dir, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# API Routes
app.include_router(predict.router)
app.include_router(feedback.router)

# Page Routes
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "page": "home", "now": datetime.now()})

@app.get("/product")
async def product(request: Request):
    return templates.TemplateResponse("product.html", {"request": request, "page": "product", "now": datetime.now()})

@app.get("/how-it-works")
async def how_it_works(request: Request):
    return templates.TemplateResponse("how_it_works.html", {"request": request, "page": "how-it-works", "now": datetime.now()})

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "page": "about", "now": datetime.now()})
