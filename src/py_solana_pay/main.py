"""Main FastAPI application"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import Base, engine
from .logging_config import get_logger

# Import models to ensure tables are created
# Import routers
from .routers import accounts, auth, checkout, products, transactions

logger = get_logger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="py-solana-pay",
    description="Python implementation of Solana-Pay - A blockchain payment system",
    version="0.1.0",
)

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Mount static files
app.mount("/static", StaticFiles(directory=PROJECT_ROOT / "static"), name="static")

# Setup templates
templates = Jinja2Templates(directory=PROJECT_ROOT / "templates")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(
    transactions.router, prefix="/api/transactions", tags=["transactions"]
)
app.include_router(checkout.router, prefix="/api/checkout", tags=["checkout"])


# Web routes (Frontend)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Homepage"""
    logger.info("Homepage accessed")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    logger.info("Login page accessed")
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page"""
    logger.info("Registration page accessed")
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "message": "Welcome to py-solana-pay API!",
        "description": "Python implementation of Solana-Pay - A blockchain payment system",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
