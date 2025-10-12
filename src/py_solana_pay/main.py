"""Main FastAPI application"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastui import prebuilt_html

from .database import Base, engine
from .logging_config import get_logger

# Import models to ensure tables are created
# Import routers
from .routers import accounts, auth, checkout, fastui_pages, products, transactions

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

# Mount static files from resources directory (for any remaining static assets)
RESOURCES_DIR = PROJECT_ROOT / "resources"
if (RESOURCES_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=RESOURCES_DIR / "static"), name="static")
    logger.info(f"Mounted static files from {RESOURCES_DIR / 'static'}")
else:
    # Fallback to original static directory if resources not available
    if (PROJECT_ROOT / "static").exists():
        app.mount(
            "/static", StaticFiles(directory=PROJECT_ROOT / "static"), name="static"
        )
        logger.info(f"Mounted static files from {PROJECT_ROOT / 'static'}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - order matters for route matching
# Data APIs with specific prefixes
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(accounts.router, prefix="/api/data/accounts", tags=["accounts"])
app.include_router(products.router, prefix="/api/data/products", tags=["products"])
app.include_router(
    transactions.router, prefix="/api/data/transactions", tags=["transactions"]
)
app.include_router(checkout.router, prefix="/api/checkout", tags=["checkout"])

# FastUI frontend router (includes /api/* for components)
app.include_router(fastui_pages.router, tags=["frontend"])


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# FastUI HTML pages - specific routes for each page
@app.get("/", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
@app.get("/register", response_class=HTMLResponse)
@app.get("/products", response_class=HTMLResponse)
@app.get("/product/{product_id}", response_class=HTMLResponse)
@app.get("/about", response_class=HTMLResponse)
@app.get("/account", response_class=HTMLResponse)
@app.get("/transactions", response_class=HTMLResponse)
@app.get("/create-product", response_class=HTMLResponse)
async def fastui_html() -> HTMLResponse:
    """Serve FastUI frontend HTML"""
    return HTMLResponse(prebuilt_html(title="Solana Pay", api_root_url="/api"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
