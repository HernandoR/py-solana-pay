"""Main FastAPI application"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
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
    return HTMLResponse(prebuilt_html(title="Solana Pay", api_root_url="/api"))


# Web routes (Frontend) - Redirects to FastUI


@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
async def index():
    """Homepage - redirects to FastUI"""
    logger.info("Homepage accessed - redirecting to FastUI")
    return RedirectResponse(url="/ui/", status_code=302)


@app.get("/login", response_class=HTMLResponse)
async def login_page():
    """Login page - redirects to FastUI"""
    logger.info("Login page accessed - redirecting to FastUI")
    return RedirectResponse(url="/ui/login", status_code=302)


@app.get("/register", response_class=HTMLResponse)
@app.get("/register.html", response_class=HTMLResponse)
async def register_page():
    """Registration page - redirects to FastUI"""
    logger.info("Registration page accessed - redirecting to FastUI")
    return RedirectResponse(url="/ui/register", status_code=302)


@app.get("/account", response_class=HTMLResponse)
async def account_page():
    """Account page - redirects to FastUI"""
    logger.info("Account page accessed - redirecting to FastUI")
    return RedirectResponse(url="/ui/account", status_code=302)


@app.get("/about", response_class=HTMLResponse)
async def about_page():
    """About page - redirects to FastUI"""
    logger.info("About page accessed - redirecting to FastUI")
    return RedirectResponse(url="/ui/about", status_code=302)


@app.get("/product", response_class=HTMLResponse)
async def product_page():
    """Product page - redirects to FastUI"""
    logger.info("Product page accessed - redirecting to FastUI")
    return RedirectResponse(url="/ui/products", status_code=302)


@app.get("/cart", response_class=HTMLResponse)
async def cart_page():
    """Shopping cart page - redirects to FastUI"""
    logger.info("Cart page accessed - redirecting to FastUI")
    return RedirectResponse(url="/ui/", status_code=302)


@app.get("/shop-single", response_class=HTMLResponse)
async def shop_single_page():
    """Shop single product page - redirects to FastUI"""
    logger.info("Shop single page accessed - redirecting to FastUI")
    return RedirectResponse(url="/ui/products", status_code=302)


@app.get("/success", response_class=HTMLResponse)
async def success_page():
    """Payment success page - redirects to FastUI"""
    logger.info("Success page accessed - redirecting to FastUI")
    return RedirectResponse(url="/ui/", status_code=302)


@app.get("/cancel", response_class=HTMLResponse)
async def cancel_page():
    """Payment cancel page - redirects to FastUI"""
    logger.info("Cancel page accessed - redirecting to FastUI")
    return RedirectResponse(url="/ui/", status_code=302)


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
