"""Main FastAPI application"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

# Mount static files from resources directory (contains frontend assets from VietBx23/Solona-Pay)
RESOURCES_DIR = PROJECT_ROOT / "resources"
if (RESOURCES_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=RESOURCES_DIR / "static"), name="static")
    logger.info(f"Mounted static files from {RESOURCES_DIR / 'static'}")
else:
    # Fallback to original static directory if resources not available
    if (PROJECT_ROOT / "static").exists():
        app.mount("/static", StaticFiles(directory=PROJECT_ROOT / "static"), name="static")
        logger.info(f"Mounted static files from {PROJECT_ROOT / 'static'}")

# Setup templates from resources directory (Thymeleaf templates converted to Jinja2)
TEMPLATES_DIR = RESOURCES_DIR / "templates" if (RESOURCES_DIR / "templates").exists() else PROJECT_ROOT / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR)
logger.info(f"Using templates from {TEMPLATES_DIR}")

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

# FastUI frontend router
app.include_router(fastui_pages.router, tags=["frontend"])


# FastUI HTML page - serves the React frontend
@app.get("/ui/{path:path}", response_class=HTMLResponse)
async def fastui_html(path: str = "") -> HTMLResponse:
    """Serve FastUI frontend HTML"""
    return HTMLResponse(prebuilt_html(title="Solana Pay"))


# Web routes (Frontend)
@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
async def index(request: Request):
    """Homepage - using resources from VietBx23/Solona-Pay"""
    logger.info("Homepage accessed")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    logger.info("Login page accessed")
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
@app.get("/register.html", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page"""
    logger.info("Registration page accessed")
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/account", response_class=HTMLResponse)
async def account_page(request: Request):
    """Account page"""
    logger.info("Account page accessed")
    return templates.TemplateResponse("account.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About page"""
    logger.info("About page accessed")
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/product", response_class=HTMLResponse)
async def product_page(request: Request):
    """Product page"""
    logger.info("Product page accessed")
    return templates.TemplateResponse("product.html", {"request": request})


@app.get("/cart", response_class=HTMLResponse)
async def cart_page(request: Request):
    """Shopping cart page"""
    logger.info("Cart page accessed")
    return templates.TemplateResponse("cart.html", {"request": request})


@app.get("/shop-single", response_class=HTMLResponse)
async def shop_single_page(request: Request):
    """Shop single product page"""
    logger.info("Shop single page accessed")
    return templates.TemplateResponse("shop-single.html", {"request": request})


@app.get("/success", response_class=HTMLResponse)
async def success_page(request: Request):
    """Payment success page"""
    logger.info("Success page accessed")
    return templates.TemplateResponse("success.html", {"request": request})


@app.get("/cancel", response_class=HTMLResponse)
async def cancel_page(request: Request):
    """Payment cancel page"""
    logger.info("Cancel page accessed")
    return templates.TemplateResponse("cancel.html", {"request": request})


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
