"""FastUI frontend router - Minimal working example"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import GoToEvent, PageEvent
from fastui.forms import FormResponse, fastui_form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.account import Account
from ..models.product import Product

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


# Dependency injection
db_dependency = Annotated[Session, Depends(get_db)]


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
    elif path == "about":
        return get_about_page()
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


def get_navbar() -> AnyComponent:
    """Common navigation bar for all pages"""
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
        end_links=[
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
        ],
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
                    submit_trigger=PageEvent(name="login-submitted"),
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
                    submit_trigger=PageEvent(name="register-submitted"),
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
    products = db.query(Product).limit(20).all()
    
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
                            on_click=PageEvent(name="view-product", data={"id": product.id}),
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
                c.Div(components=product_components, class_name="products-grid"),
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
async def login_submit(form: Annotated[LoginForm, fastui_form(LoginForm)]) -> FormResponse:
    """Handle login form submission"""
    # TODO: Implement actual authentication
    # For now, just redirect to index
    return FormResponse(
        event=GoToEvent(url="/ui/"),
        # In real implementation, validate credentials and set auth token
    )


@router.post("/ui/api/register/submit")
async def register_submit(
    form: Annotated[RegisterForm, fastui_form(RegisterForm)], db: db_dependency
) -> FormResponse:
    """Handle registration form submission"""
    # TODO: Implement actual registration logic
    # For now, just redirect to login
    return FormResponse(
        event=GoToEvent(url="/ui/login"),
        # In real implementation, create account and redirect
    )
