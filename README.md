# py-solana-pay

Python implementation of Solana-Pay - A blockchain payment system built on the Solana platform, focusing on improving security and privacy in transactions.

This project is a Python port of the original [VietBx23/Solona-Pay](https://github.com/VietBx23/Solona-Pay) Java Spring Boot application.

## Features

- **Transaction Security:** Utilizes advanced encryption technologies and security methods to ensure the integrity and safety of transactions
- **Privacy:** Conceals identification information and personal details during transactions
- **Scalability and Compatibility:** Compatible with the overall infrastructure of the Solana blockchain
- **Integration with Wallets:** Easily integrates with cryptocurrency wallets and other applications
- **Credit Card Payments:** Connects with credit cards to expand payment options (via CandyPay)
- **RESTful API:** FastAPI-based REST API for easy integration
- **Authentication:** JWT-based authentication system
- **Database Support:** SQLAlchemy ORM with SQLite default (configurable for PostgreSQL, MySQL)

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -e .
   ```

2. **Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

4. **Access the API**
   - API Server: http://localhost:8000
   - Interactive API Documentation: http://localhost:8000/docs
   - Alternative API Documentation: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/token` - Login and get access token
- `GET /api/auth/me` - Get current user profile

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}` - Get product by ID
- `POST /api/products/` - Create new product (authenticated)
- `PUT /api/products/{id}` - Update product (authenticated)
- `DELETE /api/products/{id}` - Delete product (authenticated)

### Transactions
- `GET /api/transactions/` - Get user's transactions
- `GET /api/transactions/{id}` - Get transaction by ID
- `POST /api/transactions/` - Create new transaction

### Checkout & Payments
- `POST /api/checkout/session` - Create payment session with CandyPay
- `POST /api/checkout/payment-url` - Generate Solana payment URL
- `POST /api/checkout/verify-payment` - Verify Solana payment

### Accounts
- `GET /api/accounts/` - List accounts
- `GET /api/accounts/{username}` - Get account by username
- `PUT /api/accounts/{username}` - Update account

## Database Models

The application includes the following database models:

- **Account** - User accounts with Solana wallet integration
- **Product** - Product catalog
- **Transaction** - Payment and transaction records
- **BankAccount** - Traditional bank account information
- **Authorities/Role** - User roles and permissions
- **Comment/Reply** - Product reviews and comments

## Development

### Project Structure
```
src/py_solana_pay/
├── __init__.py
├── main.py              # FastAPI application
├── database.py          # Database configuration
├── models/              # SQLAlchemy models
│   ├── account.py
│   ├── product.py
│   ├── transaction.py
│   └── ...
└── routers/             # API route handlers
    ├── auth.py
    ├── products.py
    ├── transactions.py
    └── ...
```

### Adding New Features

1. Create database models in `src/py_solana_pay/models/`
2. Add API routes in `src/py_solana_pay/routers/`
3. Register routers in `main.py`
4. Update database migrations if needed

## Configuration

Key environment variables:

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT signing secret
- `CANDYPAY_PRIVATE_API_KEY` - CandyPay private API key
- `CANDYPAY_PUBLIC_API_KEY` - CandyPay public API key
- `CANDYPAY_ENDPOINT` - CandyPay API endpoint

## Contributing

This project is a learning implementation of Solana Pay in Python. Contributions are welcome!

## Acknowledgments

This project is a Python implementation inspired by and ported from the original [VietBx23/Solona-Pay](https://github.com/VietBx23/Solona-Pay) Java Spring Boot application.

**Special thanks to:**
- **[VietBx23](https://github.com/VietBx23)** - For creating the original Solona-Pay project and providing the frontend resources, design inspiration, and overall architecture that made this Python port possible.
- The frontend templates, CSS, JavaScript, and static assets in the `resources/` directory are adapted from the original VietBx23/Solona-Pay repository.

We are deeply grateful for their excellent work and for making their project available as a reference.

## License

This project is inspired by and ported from [VietBx23/Solona-Pay](https://github.com/VietBx23/Solona-Pay).
