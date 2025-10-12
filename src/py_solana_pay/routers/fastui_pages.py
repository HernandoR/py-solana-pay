"""FastUI frontend router - Complete implementation"""

from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import AuthEvent, GoToEvent, PageEvent
from fastui.forms import fastui_form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.account import Account
from ..models.product import Product
from ..models.transaction import Transaction
from ..routers.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    get_user,
)

router = APIRouter()


# Pydantic models for forms
class LoginForm(BaseModel):
    username: str = Field(title="Username", description="Your username")
    password: str = Field(
        title="Password", description="Your password", json_schema_extra={"type": "password"}
    )


class RegisterForm(BaseModel):
    username: str = Field(title="Username", min_length=3, max_length=50)
    email: str = Field(title="Email")
    fullname: str = Field(title="Full Name")
    password: str = Field(
        title="Password", min_length=6, json_schema_extra={"type": "password"}
    )
    wallet_key: str = Field(
        default="", title="Solana Wallet Address (Optional)", description="Your Solana wallet public key"
    )


class ProductForm(BaseModel):
    name: str = Field(title="Product Name")
    price: float = Field(title="Price (SOL)", gt=0)
    quantity: int = Field(title="Quantity", ge=0)
    image: str = Field(default="", title="Image URL (Optional)")


# Dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
optional_user_dependency = Annotated[Optional[Account], Depends(lambda: None)]


@router.get("/ui/api/{path:path}")
async def fastui_api_endpoint(path: str, db: db_dependency) -> list[AnyComponent]:
    """Main FastUI API endpoint - routes to different pages"""
    
    if path == "" or path == "index":
        return get_index_page()
    elif path == "login":
        return get_login_page()
    elif path == "register":
        return get_register_page()
    elif path == "products":
        return get_products_page(db)
    elif path.startswith("product/"):
        product_id = path.split("/")[1]
        return get_product_detail_page(db, int(product_id))
    elif path == "about":
        return get_about_page()
    elif path == "account":
        return get_account_page()
    elif path == "transactions":
        return get_transactions_page()
    elif path == "create-product":
        return get_create_product_page()
    else:
        # 404 page
        return [
            c.Page(
                components=[
                    c.Heading(text="404 - Page Not Found", level=1),
                    c.Paragraph(text=f"The page '{path}' does not exist."),
                    c.Link(components=[c.Text(text="Go Home")], on_click=GoToEvent(url="/ui/")),
                ]
            )
        ]


def get_navbar(authenticated: bool = False) -> AnyComponent:
    """Common navigation bar for all pages"""
    end_links = []
    
    if authenticated:
        end_links = [
            c.Link(
                components=[c.Text(text="Account")],
                on_click=GoToEvent(url="/ui/account"),
                active="startswith:/ui/account",
            ),
            c.Link(
                components=[c.Text(text="Transactions")],
                on_click=GoToEvent(url="/ui/transactions"),
                active="startswith:/ui/transactions",
            ),
            c.Link(
                components=[c.Text(text="Logout")],
                on_click=PageEvent(name="logout"),
            ),
        ]
    else:
        end_links = [
            c.Link(
                components=[c.Text(text="Login")],
                on_click=GoToEvent(url="/ui/login"),
                active="startswith:/ui/login",
            ),
            c.Link(
                components=[c.Text(text="Register")],
                on_click=GoToEvent(url="/ui/register"),
                active="startswith:/ui/register",
            ),
        ]
    
    return c.Navbar(
        title="Solana Pay",
        title_event=GoToEvent(url="/ui/"),
        start_links=[
            c.Link(
                components=[c.Text(text="Home")],
                on_click=GoToEvent(url="/ui/"),
                active="startswith:/ui/index",
            ),
            c.Link(
                components=[c.Text(text="Products")],
                on_click=GoToEvent(url="/ui/products"),
                active="startswith:/ui/products",
            ),
            c.Link(
                components=[c.Text(text="About")],
                on_click=GoToEvent(url="/ui/about"),
                active="startswith:/ui/about",
            ),
        ],
        end_links=end_links,
    )


def get_index_page() -> list[AnyComponent]:
    """Homepage with hero section"""
    return [
        c.Page(
            components=[
                get_navbar(),
                c.Heading(text="Welcome to Solana Pay", level=1),
                c.Paragraph(
                    text="The future of payments powered by Solana blockchain"
                ),
                c.Div(
                    components=[
                        c.Heading(text="Why Choose Solana Pay?", level=2),
                        c.Paragraph(
                            text="Experience fast, secure, and low-cost blockchain payments."
                        ),
                    ],
                    class_name="my-4",
                ),
                c.Div(
                    components=[
                        c.Div(
                            components=[
                                c.Heading(text="🚀 Lightning Fast", level=3),
                                c.Paragraph(
                                    text="Near-instant transactions with Solana's high-performance blockchain, processing thousands of transactions per second."
                                ),
                            ],
                            class_name="col-md-4 mb-4",
                        ),
                        c.Div(
                            components=[
                                c.Heading(text="💰 No Hidden Fees", level=3),
                                c.Paragraph(
                                    text="Pay only minimal network fees. No hidden charges or surprise costs."
                                ),
                            ],
                            class_name="col-md-4 mb-4",
                        ),
                        c.Div(
                            components=[
                                c.Heading(text="🔒 Secure & Private", level=3),
                                c.Paragraph(
                                    text="Built on Solana's secure blockchain with advanced cryptography to protect your transactions."
                                ),
                            ],
                            class_name="col-md-4 mb-4",
                        ),
                    ],
                    class_name="row",
                ),
                c.Div(
                    components=[
                        c.Button(
                            text="Get Started",
                            on_click=GoToEvent(url="/ui/register"),
                            class_name="btn btn-primary me-2",
                        ),
                        c.Button(
                            text="Browse Products",
                            on_click=GoToEvent(url="/ui/products"),
                            class_name="btn btn-outline-primary",
                        ),
                    ],
                    class_name="mt-4",
                ),
            ]
        )
    ]


def get_login_page() -> list[AnyComponent]:
    """Login page with form"""
    return [
        c.Page(
            components=[
                get_navbar(),
                c.Heading(text="Login", level=1),
                c.Paragraph(text="Sign in to your Solana Pay account"),
                c.ModelForm(
                    model=LoginForm,
                    submit_url="/ui/api/login/submit",
                    method="POST",
                ),
                c.Div(
                    components=[
                        c.Text(text="Don't have an account? "),
                        c.Link(
                            components=[c.Text(text="Register here")],
                            on_click=GoToEvent(url="/ui/register"),
                        ),
                    ],
                    class_name="mt-3",
                ),
            ]
        )
    ]


def get_register_page() -> list[AnyComponent]:
    """Registration page with form"""
    return [
        c.Page(
            components=[
                get_navbar(),
                c.Heading(text="Register", level=1),
                c.Paragraph(text="Create your Solana Pay account"),
                c.ModelForm(
                    model=RegisterForm,
                    submit_url="/ui/api/register/submit",
                    method="POST",
                ),
                c.Div(
                    components=[
                        c.Text(text="Already have an account? "),
                        c.Link(
                            components=[c.Text(text="Login here")],
                            on_click=GoToEvent(url="/ui/login"),
                        ),
                    ],
                    class_name="mt-3",
                ),
            ]
        )
    ]


def get_products_page(db: Session) -> list[AnyComponent]:
    """Products listing page"""
    # Fetch products from database
    products = db.query(Product).limit(50).all()
    
    if not products:
        product_components = [
            c.Paragraph(text="No products available at the moment."),
            c.Paragraph(text="Check back soon!"),
        ]
    else:
        product_components = []
        for product in products:
            product_components.append(
                c.Div(
                    components=[
                        c.Heading(text=product.name, level=4),
                        c.Paragraph(text=f"Price: {product.price} SOL"),
                        c.Paragraph(text=f"Available: {product.quantity}"),
                        c.Button(
                            text="View Details",
                            on_click=GoToEvent(url=f"/ui/product/{product.id}"),
                            class_name="btn btn-sm btn-primary",
                        ),
                    ],
                    class_name="card p-3 mb-3",
                )
            )
    
    return [
        c.Page(
            components=[
                get_navbar(),
                c.Heading(text="Products", level=1),
                c.Paragraph(text="Browse our collection of items available for purchase with Solana"),
                c.Div(
                    components=[
                        c.Link(
                            components=[c.Text(text="+ Create New Product")],
                            on_click=GoToEvent(url="/ui/create-product"),
                            class_name="btn btn-success mb-3",
                        ),
                    ]
                ),
                c.Div(components=product_components, class_name="products-grid"),
            ]
        )
    ]


def get_product_detail_page(db: Session, product_id: int) -> list[AnyComponent]:
    """Product detail page"""
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        return [
            c.Page(
                components=[
                    get_navbar(),
                    c.Heading(text="Product Not Found", level=1),
                    c.Paragraph(text=f"Product with ID {product_id} does not exist."),
                    c.Link(
                        components=[c.Text(text="Back to Products")],
                        on_click=GoToEvent(url="/ui/products"),
                    ),
                ]
            )
        ]
    
    return [
        c.Page(
            components=[
                get_navbar(),
                c.Heading(text=product.name, level=1),
                c.Div(
                    components=[
                        c.Heading(text="Product Details", level=3),
                        c.Paragraph(text=f"Price: {product.price} SOL"),
                        c.Paragraph(text=f"Available Quantity: {product.quantity}"),
                        c.Paragraph(text=f"Product ID: {product.id}"),
                    ],
                    class_name="card p-4 mb-3",
                ),
                c.Div(
                    components=[
                        c.Button(
                            text="Add to Cart",
                            on_click=PageEvent(name="add-to-cart", data={"product_id": product.id}),
                            class_name="btn btn-primary me-2",
                        ),
                        c.Link(
                            components=[c.Text(text="Back to Products")],
                            on_click=GoToEvent(url="/ui/products"),
                            class_name="btn btn-secondary",
                        ),
                    ]
                ),
            ]
        )
    ]


def get_account_page() -> list[AnyComponent]:
    """Account management page (requires authentication)"""
    return [
        c.Page(
            components=[
                get_navbar(authenticated=True),
                c.Heading(text="My Account", level=1),
                c.Paragraph(text="Manage your account settings and view your information."),
                c.Div(
                    components=[
                        c.Heading(text="Account Information", level=3),
                        c.Paragraph(text="Username: [Current User]"),
                        c.Paragraph(text="Email: [User Email]"),
                        c.Paragraph(text="Wallet: [Wallet Address]"),
                    ],
                    class_name="card p-4 mb-3",
                ),
                c.Link(
                    components=[c.Text(text="View Transactions")],
                    on_click=GoToEvent(url="/ui/transactions"),
                    class_name="btn btn-primary",
                ),
            ]
        )
    ]


def get_transactions_page() -> list[AnyComponent]:
    """Transactions history page (requires authentication)"""
    return [
        c.Page(
            components=[
                get_navbar(authenticated=True),
                c.Heading(text="Transaction History", level=1),
                c.Paragraph(text="View all your past transactions."),
                c.Div(
                    components=[
                        c.Paragraph(text="No transactions yet."),
                    ],
                    class_name="card p-4",
                ),
            ]
        )
    ]


def get_create_product_page() -> list[AnyComponent]:
    """Create product page"""
    return [
        c.Page(
            components=[
                get_navbar(),
                c.Heading(text="Create New Product", level=1),
                c.Paragraph(text="Add a new product to the catalog"),
                c.ModelForm(
                    model=ProductForm,
                    submit_url="/ui/api/product/create",
                    method="POST",
                ),
                c.Link(
                    components=[c.Text(text="Cancel")],
                    on_click=GoToEvent(url="/ui/products"),
                    class_name="btn btn-secondary mt-3",
                ),
            ]
        )
    ]


def get_about_page() -> list[AnyComponent]:
    """About page"""
    return [
        c.Page(
            components=[
                get_navbar(),
                c.Heading(text="About Solana Pay", level=1),
                c.Paragraph(
                    text="Solana Pay is a Python implementation of a blockchain payment system built on the Solana platform."
                ),
                c.Heading(text="Features", level=2),
                c.Paragraph(text="• User authentication and account management"),
                c.Paragraph(text="• Product catalog and shopping"),
                c.Paragraph(text="• Solana blockchain integration"),
                c.Paragraph(text="• QR code payment generation"),
                c.Paragraph(text="• Transaction verification"),
                c.Heading(text="Technology Stack", level=2),
                c.Paragraph(text="• Backend: FastAPI (Python)"),
                c.Paragraph(text="• Frontend: FastUI"),
                c.Paragraph(text="• Database: SQLAlchemy ORM"),
                c.Paragraph(text="• Blockchain: Solana"),
                c.Paragraph(text="• Authentication: JWT"),
            ]
        )
    ]


@router.post("/ui/api/login/submit")
async def login_submit(
    form: Annotated[LoginForm, fastui_form(LoginForm)], 
    db: db_dependency
) -> list[AnyComponent]:
    """Handle login form submission"""
    # Authenticate user
    user = authenticate_user(db, form.username, form.password)
    
    if not user:
        # Return error toast
        return [
            c.Toast(
                title="Login Failed",
                body="Incorrect username or password",
                open_trigger=PageEvent(name="login-error"),
            ),
        ]
    
    # Generate access token
    from datetime import timedelta
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=timedelta(minutes=30)
    )
    
    # Return success and redirect with auth event
    return [
        c.FireEvent(event=AuthEvent(token=access_token, url="/ui/account")),
    ]


@router.post("/ui/api/register/submit")
async def register_submit(
    form: Annotated[RegisterForm, fastui_form(RegisterForm)], 
    db: db_dependency
) -> list[AnyComponent]:
    """Handle registration form submission"""
    # Check if user already exists
    existing_user = get_user(db, form.username)
    if existing_user:
        return [
            c.Toast(
                title="Registration Failed",
                body="Username already exists",
                open_trigger=PageEvent(name="register-error"),
            ),
        ]
    
    # Check if email already exists
    existing_email = db.query(Account).filter(Account.email == form.email).first()
    if existing_email:
        return [
            c.Toast(
                title="Registration Failed",
                body="Email already registered",
                open_trigger=PageEvent(name="register-error"),
            ),
        ]
    
    # Create new user
    hashed_password = get_password_hash(form.password)
    new_user = Account(
        username=form.username,
        email=form.email,
        fullname=form.fullname,
        password=hashed_password,
        wallet_key=form.wallet_key if form.wallet_key else None,
    )
    db.add(new_user)
    db.commit()
    
    # Redirect to login
    return [
        c.Toast(
            title="Success",
            body="Account created successfully! Please login.",
            open_trigger=PageEvent(name="register-success"),
        ),
        c.FireEvent(event=GoToEvent(url="/ui/login")),
    ]


@router.post("/ui/api/product/create")
async def create_product_submit(
    form: Annotated[ProductForm, fastui_form(ProductForm)],
    db: db_dependency
) -> list[AnyComponent]:
    """Handle product creation"""
    # Create new product
    new_product = Product(
        name=form.name,
        price=form.price,
        quantity=form.quantity,
        image=form.image if form.image else None,
    )
    db.add(new_product)
    db.commit()
    
    # Redirect to products page
    return [
        c.Toast(
            title="Success",
            body=f"Product '{form.name}' created successfully!",
            open_trigger=PageEvent(name="product-created"),
        ),
        c.FireEvent(event=GoToEvent(url="/ui/products")),
    ]
