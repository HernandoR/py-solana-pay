# Backend Behavior Description

## Overview
The backend is a FastAPI-based REST API that provides authentication, product management, payment processing, and transaction tracking for the py-solana-pay platform. It integrates with the Solana blockchain for cryptocurrency payments.

## Architecture

### Technology Stack
- **Framework**: FastAPI (Python 3.10+)
- **Database**: SQLAlchemy ORM with SQLite (configurable to PostgreSQL/MySQL)
- **Authentication**: JWT (JSON Web Tokens) with OAuth2
- **Password Hashing**: bcrypt via passlib
- **Blockchain**: Solana via solana-py library
- **Payment Provider**: CandyPay (optional)
- **QR Code Generation**: qrcode library
- **HTTP Client**: httpx for async requests

### Project Structure
```
src/py_solana_pay/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration and session management
├── logging_config.py       # Logging setup
├── solana_integration.py   # Solana blockchain integration
├── models/                 # SQLAlchemy ORM models
│   ├── account.py          # User account model
│   ├── product.py          # Product model
│   ├── transaction.py      # Transaction model
│   ├── bank_account.py     # Bank account model
│   ├── comment.py          # Comment model
│   ├── reply.py            # Reply model
│   ├── role.py             # Role model
│   └── authorities.py      # Authority/permission model
├── routers/                # API route handlers
│   ├── auth.py             # Authentication endpoints
│   ├── accounts.py         # Account management endpoints
│   ├── products.py         # Product management endpoints
│   ├── transactions.py     # Transaction endpoints
│   └── checkout.py         # Payment/checkout endpoints
└── schemas/                # Pydantic models for request/response
    ├── payment.py          # Payment-related schemas
    └── account.py          # Account-related schemas
```

## API Endpoints

### Authentication (`/api/auth`)

#### POST `/api/auth/register`
**Purpose**: Register a new user account
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "fullname": "string",
    "password": "string",
    "wallet_key": "string (optional)"
  }
  ```
- **Response**: `201 Created`
  ```json
  {
    "username": "string",
    "email": "string",
    "fullname": "string",
    "wallet_key": "string or null"
  }
  ```
- **Errors**:
  - `400`: Username or email already registered
- **Behavior**:
  - Validates unique username and email
  - Hashes password using bcrypt
  - Creates account record in database
  - Returns user information (without password)

#### POST `/api/auth/token`
**Purpose**: Login and obtain JWT access token
- **Request Body**: Form data
  ```
  username=string&password=string
  ```
- **Response**: `200 OK`
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```
- **Errors**:
  - `401`: Invalid credentials
- **Behavior**:
  - Validates username and password
  - Generates JWT token (30-minute expiration)
  - Returns token for subsequent authenticated requests

#### GET `/api/auth/me`
**Purpose**: Get current authenticated user profile
- **Headers**: `Authorization: Bearer {token}`
- **Response**: `200 OK`
  ```json
  {
    "username": "string",
    "email": "string",
    "fullname": "string",
    "wallet_key": "string or null"
  }
  ```
- **Errors**:
  - `401`: Invalid or missing token
- **Behavior**:
  - Decodes and validates JWT token
  - Returns current user information

### Products (`/api/products`)

#### GET `/api/products/`
**Purpose**: List all products
- **Query Parameters**:
  - `skip`: int (offset for pagination, default 0)
  - `limit`: int (max items to return, default 100)
- **Response**: `200 OK`
  ```json
  [
    {
      "id": 1,
      "name": "string",
      "price": 0.0,
      "image": "string or null",
      "quantity": 0
    }
  ]
  ```
- **Behavior**:
  - Returns paginated list of products
  - No authentication required

#### GET `/api/products/{product_id}`
**Purpose**: Get single product by ID
- **Path Parameter**: `product_id` (integer)
- **Response**: `200 OK` (same structure as list item)
- **Errors**:
  - `404`: Product not found
- **Behavior**:
  - Returns product details
  - No authentication required

#### POST `/api/products/`
**Purpose**: Create new product (authenticated)
- **Headers**: `Authorization: Bearer {token}`
- **Request Body**:
  ```json
  {
    "name": "string",
    "price": 0.0,
    "image": "string (optional)",
    "quantity": 0
  }
  ```
- **Response**: `201 Created`
- **Errors**:
  - `401`: Not authenticated
- **Behavior**:
  - Requires authentication
  - Creates product in database
  - Returns created product

#### PUT `/api/products/{product_id}`
**Purpose**: Update existing product (authenticated)
- **Headers**: `Authorization: Bearer {token}`
- **Path Parameter**: `product_id` (integer)
- **Request Body**: Partial update allowed
  ```json
  {
    "name": "string (optional)",
    "price": 0.0 (optional),
    "image": "string (optional)",
    "quantity": 0 (optional)
  }
  ```
- **Response**: `200 OK`
- **Errors**:
  - `401`: Not authenticated
  - `404`: Product not found
- **Behavior**:
  - Updates only provided fields
  - Returns updated product

#### DELETE `/api/products/{product_id}`
**Purpose**: Delete product (authenticated)
- **Headers**: `Authorization: Bearer {token}`
- **Path Parameter**: `product_id` (integer)
- **Response**: `200 OK`
  ```json
  {"message": "Product deleted successfully"}
  ```
- **Errors**:
  - `401`: Not authenticated
  - `404`: Product not found

### Transactions (`/api/transactions`)

#### GET `/api/transactions/`
**Purpose**: Get current user's transactions
- **Headers**: `Authorization: Bearer {token}`
- **Query Parameters**:
  - `skip`: int (default 0)
  - `limit`: int (default 100)
- **Response**: `200 OK`
  ```json
  [
    {
      "transaction_id": 1,
      "transaction_type": "string",
      "transaction_details": "string",
      "transaction_date": "2024-01-01T12:00:00",
      "username": "string"
    }
  ]
  ```
- **Behavior**:
  - Returns only transactions belonging to authenticated user
  - Paginated results

#### GET `/api/transactions/{transaction_id}`
**Purpose**: Get specific transaction by ID
- **Headers**: `Authorization: Bearer {token}`
- **Path Parameter**: `transaction_id` (integer)
- **Response**: `200 OK` (same structure as list item)
- **Errors**:
  - `401`: Not authenticated
  - `403`: Not authorized (transaction belongs to different user)
  - `404`: Transaction not found
- **Behavior**:
  - Validates user owns the transaction
  - Returns transaction details

#### POST `/api/transactions/`
**Purpose**: Create new transaction record
- **Headers**: `Authorization: Bearer {token}`
- **Request Body**:
  ```json
  {
    "transaction_type": "string",
    "transaction_details": "string (optional)"
  }
  ```
- **Response**: `201 Created`
- **Behavior**:
  - Automatically associates with authenticated user
  - Sets transaction_date to current UTC time

### Checkout & Payment (`/api/checkout`)

#### POST `/api/checkout/session`
**Purpose**: Create payment session with CandyPay
- **Headers**: `Authorization: Bearer {token}`
- **Request Body**: Dict of session parameters
- **Response**: `200 OK`
  ```json
  {
    "session_id": "string",
    "order_id": "string"
  }
  ```
- **Errors**:
  - `401`: Not authenticated
  - `500`: CandyPay API error or not configured
- **Behavior**:
  - Creates session with CandyPay payment provider
  - Records transaction in database
  - Returns session identifiers

#### POST `/api/checkout/payment-url`
**Purpose**: Generate Solana payment URL and QR code
- **Headers**: `Authorization: Bearer {token}`
- **Request Body**:
  ```json
  {
    "recipient": "string (Solana wallet address)",
    "amount": 0.0,
    "label": "string (optional)",
    "message": "string (optional)",
    "memo": "string (optional)"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "payment_url": "solana:...",
    "qr_code_url": "data:image/png;base64,..."
  }
  ```
- **Errors**:
  - `400`: Invalid parameters
  - `401`: Not authenticated
  - `500`: QR code generation failed
- **Behavior**:
  - Generates Solana Pay protocol URL
  - Creates QR code for mobile wallet scanning
  - Records URL generation in transaction history

#### POST `/api/checkout/verify-payment`
**Purpose**: Verify Solana blockchain transaction
- **Headers**: `Authorization: Bearer {token}`
- **Request Body**:
  ```json
  {
    "signature": "string (transaction signature)",
    "expected_recipient": "string (wallet address)",
    "expected_amount": 0.0
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "verified": true,
    "signature": "string",
    "amount": 0.0,
    "recipient": "string",
    "timestamp": "string",
    "message": "string"
  }
  ```
- **Behavior**:
  - Queries Solana blockchain for transaction
  - Validates recipient and amount match expectations
  - Records verification attempt
  - Returns verification result (even on failure)

#### GET `/api/checkout/balance/{address}`
**Purpose**: Get SOL balance for wallet address
- **Headers**: `Authorization: Bearer {token}`
- **Path Parameter**: `address` (Solana wallet address)
- **Response**: `200 OK`
  ```json
  {
    "address": "string",
    "balance": 0.0,
    "currency": "SOL"
  }
  ```
- **Errors**:
  - `401`: Not authenticated
  - `404`: Could not retrieve balance
  - `500`: Balance retrieval failed

### Accounts (`/api/accounts`)

#### GET `/api/accounts/`
**Purpose**: List all accounts (admin function)
- **Query Parameters**:
  - `skip`: int (default 0)
  - `limit`: int (default 100)
- **Response**: `200 OK`
  ```json
  [
    {
      "username": "string",
      "email": "string",
      "fullname": "string",
      "wallet_key": "string or null"
    }
  ]
  ```
- **Behavior**:
  - Returns all accounts (TODO: add admin role check)

#### GET `/api/accounts/{username}`
**Purpose**: Get account by username
- **Path Parameter**: `username` (string)
- **Response**: `200 OK`
- **Errors**:
  - `404`: Account not found

#### PUT `/api/accounts/{username}`
**Purpose**: Update account information
- **Headers**: `Authorization: Bearer {token}`
- **Path Parameter**: `username` (string)
- **Request Body**:
  ```json
  {
    "email": "string (optional)",
    "fullname": "string (optional)",
    "wallet_key": "string (optional)"
  }
  ```
- **Response**: `200 OK`
- **Errors**:
  - `401`: Not authenticated
  - `403`: Not authorized (can only update own account)
  - `404`: Account not found
- **Behavior**:
  - Users can only update their own account
  - Partial updates supported

## Database Models

### Account
- `username` (Primary Key, String)
- `email` (String, Unique)
- `fullname` (String)
- `password` (String, hashed)
- `wallet_key` (String, nullable)

### Product
- `id` (Primary Key, Integer, Auto-increment)
- `name` (String)
- `price` (Float)
- `image` (String, nullable)
- `quantity` (Integer)

### Transaction
- `transaction_id` (Primary Key, Integer, Auto-increment)
- `transaction_type` (String)
- `transaction_details` (String, nullable)
- `transaction_date` (DateTime)
- `username` (Foreign Key → Account.username)

## Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string (default: SQLite)
- `SECRET_KEY`: JWT signing key (required)
- `CANDYPAY_PRIVATE_API_KEY`: CandyPay private API key (optional)
- `CANDYPAY_PUBLIC_API_KEY`: CandyPay public API key (optional)
- `CANDYPAY_ENDPOINT`: CandyPay API endpoint (optional)
- `SOLANA_RPC_URL`: Solana RPC endpoint (optional, uses public endpoint by default)

### CORS Configuration
- Currently allows all origins (`*`)
- Should be restricted in production to specific frontend domains

## Security Features

### Authentication
- JWT tokens with 30-minute expiration
- HS256 algorithm for token signing
- bcrypt password hashing with automatic salt

### Authorization
- Bearer token authentication required for most endpoints
- User can only access/modify their own data
- Admin endpoints planned (not fully implemented)

### Input Validation
- Pydantic models enforce type safety
- Email validation
- Username uniqueness
- Password strength (TODO: add requirements)

## Solana Integration

### Payment URL Generation
- Implements Solana Pay protocol
- URL format: `solana:{recipient}?amount={amount}&label={label}&message={message}&memo={memo}`
- QR code generated for mobile wallet scanning

### Transaction Verification
- Queries Solana RPC for transaction details
- Validates transaction signature
- Verifies recipient and amount
- Checks transaction status

### Balance Queries
- Retrieves SOL balance for any valid address
- Uses Solana RPC endpoint

## Error Handling
- Consistent HTTP status codes
- JSON error responses with detail messages
- Exception handling for:
  - Database errors
  - Authentication failures
  - Blockchain query failures
  - Payment provider errors

## Logging
- Configured via loguru
- Logs to `logs/` directory
- Logs application events, errors, and API access

## Health & Monitoring

### GET `/health`
Simple health check endpoint
- **Response**: `200 OK`
  ```json
  {"status": "healthy"}
  ```

### GET `/api`
API information endpoint
- **Response**: `200 OK`
  ```json
  {
    "message": "Welcome to py-solana-pay API!",
    "description": "Python implementation of Solana-Pay - A blockchain payment system",
    "version": "0.1.0",
    "docs": "/docs"
  }
  ```

## API Documentation
- Interactive docs: `/docs` (Swagger UI)
- Alternative docs: `/redoc` (ReDoc)
- Automatically generated from FastAPI routes and Pydantic models

## Planned Improvements
1. Role-based access control (admin/user roles)
2. Enhanced password requirements
3. Email verification
4. Password reset functionality
5. Rate limiting
6. Enhanced transaction filtering and search
7. Webhook support for payment notifications
8. Multi-currency support
9. Product categories and tags
10. Shopping cart persistence in backend
