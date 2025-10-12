# Resources Directory

This directory contains frontend resources adapted from [VietBx23/Solona-Pay](https://github.com/VietBx23/Solona-Pay).

## Contents

### Static Assets (`static/`)
Contains all static frontend files:
- **CSS**: Bootstrap, custom styles, and component styles
- **JavaScript**: jQuery, AngularJS, custom scripts
- **Images**: Hero images, icons, and other visual assets
- **Fonts**: Icon fonts and custom fonts
- **SCSS**: Source SCSS files for Bootstrap customization

### Templates (`templates/`)
HTML templates converted from Thymeleaf to Jinja2:
- `base.html` - Base layout template (converted from `layout/layout.html`)
- `index.html` - Homepage with carousel and features
- `login.html` - Login page with form validation
- `register.html` - Registration page with Solana wallet field
- `account.html` - User account management page (admin)
- `product.html` - Product listing page with NFT cards
- `shop-single.html` - Single product detail page
- `cart.html` - Shopping cart page with AngularJS integration
- `about.html` - About page with team information
- `forget.html` - Forgot password page
- `success.html` - Payment success page
- `cancel.html` - Payment cancellation page

**Note**: Original Thymeleaf templates are in `templates.thymeleaf/` directory for reference.

### Configuration (`config.py`)
Python configuration file that maps Spring Boot `application.properties` to Python/FastAPI equivalents.

Original Spring Boot configurations have been converted to:
- Environment variables (recommended)
- Python configuration constants
- FastAPI settings

### Original Configuration (`application.properties`)
Original Spring Boot configuration file (kept for reference).

**Important**: This file uses Java/Spring Boot syntax and is not directly used by the Python application.
Use `config.py` or environment variables instead.

## Template Conversion Notes

Templates have been converted from Thymeleaf to Jinja2:

### Thymeleaf → Jinja2 Conversions:
- `th:fragment="dynamic(title, view)"` → `{% extends "base.html" %}`
- `th:replace="${view}"` → `{% block content %}{% endblock %}`
- `th:replace="${title}"` → `{% block title %}{% endblock %}`
- `th:src="@{/path}"` → `{{ url_for('static', path='path') }}`
- Thymeleaf expressions → Jinja2 template variables

### URL Updates:
- Static file references updated to use `url_for('static', path='...')`
- Route references updated to match FastAPI routes

## Usage in FastAPI

The main FastAPI application (`src/py_solana_pay/main.py`) automatically:
1. Mounts static files from `resources/static/`
2. Uses templates from `resources/templates/`
3. Serves frontend pages at appropriate routes

Example:
```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="resources/static"), name="static")
templates = Jinja2Templates(directory="resources/templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

## Acknowledgments

**Special thanks to [VietBx23](https://github.com/VietBx23)** for creating the original Solona-Pay project.

The frontend resources in this directory are adapted from:
https://github.com/VietBx23/Solona-Pay

## License

These resources maintain attribution to the original VietBx23/Solona-Pay project.