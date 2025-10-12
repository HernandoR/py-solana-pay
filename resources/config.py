"""
Configuration mapping from Spring Boot application.properties to Python settings.

This file maps the original Java Spring Boot configuration to Python/FastAPI equivalents.
Original file: resources/application.properties

Spring Boot → FastAPI/Python equivalents:
- spring.mvc.view → FastAPI templates with Jinja2
- spring.servlet.multipart → FastAPI file upload limits
- spring.datasource → SQLAlchemy database configuration
- candypay.* → Environment variables for payment integration
"""

from pathlib import Path

# View Configuration (Spring MVC → Jinja2 Templates)
# Original: spring.mvc.view.prefix = /views/
# Original: spring.mvc.view.suffix = .jsp
TEMPLATE_DIR = Path(__file__).parent / "templates"
STATIC_DIR = Path(__file__).parent / "static"

# File Upload Configuration
# Original: spring.servlet.multipart.max-file-size=20MB
# Original: spring.servlet.multipart.max-request-size=20MB
MAX_FILE_SIZE_MB = 20
MAX_REQUEST_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_REQUEST_SIZE_BYTES = MAX_REQUEST_SIZE_MB * 1024 * 1024

# Database Configuration
# Original Spring Boot used SQL Server:
# spring.datasource.url=jdbc:sqlserver://localhost;databaseName=PayPalDB;...
# spring.datasource.username=sa
# spring.datasource.password=songlong
# spring.datasource.driverClassName=com.microsoft.sqlserver.jdbc.SQLServerDriver
# spring.jpa.show-sql = true
# spring.jpa.hibernate.ddl-auto=none
# spring.jpa.database-platform= org.hibernate.dialect.SQLServer2012Dialect

# Python/SQLAlchemy equivalent configuration:
# These should be set in .env file or environment variables
# DATABASE_URL=sqlite:///./solana_pay.db  # Default SQLite
# DATABASE_URL=postgresql://user:password@localhost/paypaldb  # PostgreSQL
# DATABASE_URL=mysql+pymysql://user:password@localhost/paypaldb  # MySQL
# DATABASE_URL=mssql+pyodbc://sa:songlong@localhost/PayPalDB?driver=ODBC+Driver+17+for+SQL+Server  # SQL Server

DATABASE_CONFIG = {
    "show_sql": True,  # Equivalent to spring.jpa.show-sql
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_recycle": 3600,
}

# CandyPay Payment Integration
# Original:
# candypay.private.api.key=cp_private_bwHmBXf4_B7UA84dPsLW6aFjkFjjB2Rka
# candypay.public.api.key=cp_public_ecHjg7Uc_6gwDsez4EPi4QT6nHeGxdJwB
# candypay.endpoint=https://checkout-api.candypay.fun/api/v1

# Python equivalent: Set in .env file
# CANDYPAY_PRIVATE_API_KEY=cp_private_bwHmBXf4_B7UA84dPsLW6aFjkFjjB2Rka
# CANDYPAY_PUBLIC_API_KEY=cp_public_ecHjg7Uc_6gwDsez4EPi4QT6nHeGxdJwB
# CANDYPAY_ENDPOINT=https://checkout-api.candypay.fun/api/v1

CANDYPAY_CONFIG = {
    "endpoint": "https://checkout-api.candypay.fun/api/v1",
    "timeout": 30,
}

# Email Configuration (Currently commented out in original)
# Original Spring Boot:
# spring.mail.host=smtp.gmail.com
# spring.mail.port=587
# spring.mail.username=...
# spring.mail.password=...

# Python equivalent: Use environment variables
# MAIL_HOST=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USERNAME=your_email@gmail.com
# MAIL_PASSWORD=your_app_password
# MAIL_USE_TLS=true

EMAIL_CONFIG = {
    "enabled": False,  # Enable when configured
    "host": "smtp.gmail.com",
    "port": 587,
    "use_tls": True,
}

# OAuth2 Configuration (Currently commented out in original)
# Original Spring Boot:
# Google OAuth2
# spring.security.oauth2.client.registration.google.client-id=...
# spring.security.oauth2.client.registration.google.client-secret=...
# Facebook OAuth2
# spring.security.oauth2.client.registration.facebook.client-id=...
# spring.security.oauth2.client.registration.facebook.client-secret=...

# Python equivalent: Use environment variables
# GOOGLE_CLIENT_ID=your_google_client_id
# GOOGLE_CLIENT_SECRET=your_google_client_secret
# FACEBOOK_CLIENT_ID=your_facebook_client_id
# FACEBOOK_CLIENT_SECRET=your_facebook_client_secret

OAUTH2_CONFIG = {
    "enabled": False,  # Enable when configured
    "google": {
        "enabled": False,
        "scopes": ["openid", "email", "profile"],
    },
    "facebook": {
        "enabled": False,
        "scopes": ["email", "public_profile"],
    },
}

# Application Configuration
APP_CONFIG = {
    "title": "py-solana-pay",
    "description": "Python implementation of Solana-Pay - A blockchain payment system",
    "version": "0.1.0",
    "debug": False,  # Set to True for development
}
