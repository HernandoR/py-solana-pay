# Frontend Behavior Description

## Overview
The frontend is a web-based user interface for the py-solana-pay system, providing users with the ability to manage accounts, browse products, and process Solana-based payments. The current implementation will be migrated from traditional HTML/CSS/JS templates to FastUI for a modern, Python-based frontend.

## Current Frontend Architecture (Traditional Templates)

### Pages and Routes

#### 1. Homepage (`/`, `/index.html`)
- **Purpose**: Landing page showcasing Solana Pay platform
- **Features**:
  - Image carousel with promotional slides
  - Call-to-action buttons for login and sign-up
  - Feature highlights (No Hidden Fees, Lightning Fast, Secure Transactions)
  - Information panels about the platform

#### 2. Login Page (`/login`)
- **Purpose**: User authentication
- **Features**:
  - Username/email input field
  - Password input field
  - "Remember me" checkbox
  - Submit button
  - Link to registration page
  - Forgot password link

#### 3. Registration Page (`/register`, `/register.html`)
- **Purpose**: New user account creation
- **Features**:
  - Username input
  - Email input
  - Full name input
  - Password input
  - Confirm password input
  - Optional wallet key input
  - Terms and conditions checkbox
  - Submit button
  - Link to login page

#### 4. Account Page (`/account`)
- **Purpose**: User profile and account management
- **Features**:
  - Display user information (username, email, full name)
  - Display wallet information
  - Transaction history
  - Account settings
  - Wallet key management
  - Edit profile functionality

#### 5. Product Listing Page (`/product`)
- **Purpose**: Browse available products for purchase
- **Features**:
  - Grid/list view of products
  - Product cards showing:
    - Product image
    - Product name
    - Price (in SOL or fiat equivalent)
    - Add to cart button
  - Search and filter functionality
  - Pagination

#### 6. Product Detail Page (`/shop-single`)
- **Purpose**: Detailed view of a single product
- **Features**:
  - Large product image
  - Product name and description
  - Price display
  - Quantity selector
  - Add to cart button
  - Product specifications
  - Related products

#### 7. Shopping Cart Page (`/cart`)
- **Purpose**: Review and manage items before checkout
- **Features**:
  - List of cart items with:
    - Product image and name
    - Quantity adjuster
    - Individual price
    - Remove item button
  - Cart summary:
    - Subtotal
    - Tax/fees (blockchain fees)
    - Total amount
  - Checkout button
  - Continue shopping link

#### 8. About Page (`/about`)
- **Purpose**: Information about the platform
- **Features**:
  - Platform description
  - Mission and vision
  - Team information
  - Technology stack
  - Contact information

#### 9. Payment Success Page (`/success`)
- **Purpose**: Confirmation of successful payment
- **Features**:
  - Success message
  - Transaction ID
  - Payment details
  - Link to view transaction
  - Return to home/shop button

#### 10. Payment Cancel Page (`/cancel`)
- **Purpose**: Handle cancelled transactions
- **Features**:
  - Cancellation message
  - Reason for cancellation (if available)
  - Option to retry payment
  - Return to cart link

### Static Assets

#### CSS
- Bootstrap-based responsive design
- Custom styles for Solana branding
- Mobile-first responsive layouts

#### JavaScript
- Form validation
- Cart management (add/remove items)
- AJAX calls to backend API
- Payment flow management
- Wallet integration

#### Images
- Product images
- Promotional banners
- Platform logos and icons

## User Flows

### 1. New User Registration Flow
1. User lands on homepage
2. Clicks "Sign up" button
3. Fills registration form
4. Optionally provides Solana wallet address
5. Submits form
6. Backend validates and creates account
7. User redirected to login or auto-logged in

### 2. Login Flow
1. User navigates to login page
2. Enters credentials
3. Submits form
4. Backend validates credentials
5. JWT token issued and stored
6. User redirected to account page or previous page

### 3. Shopping Flow
1. User browses product listing
2. Clicks on product for details
3. Adds product to cart
4. Continues shopping or goes to cart
5. Reviews cart items
6. Proceeds to checkout
7. Initiates payment with Solana

### 4. Payment Flow
1. User initiates checkout from cart
2. Payment session created
3. Solana payment URL generated with QR code
4. User scans QR code with wallet app or copies payment URL
5. Completes payment in wallet
6. Backend verifies transaction on Solana blockchain
7. User redirected to success/cancel page
8. Transaction recorded in database

### 5. Account Management Flow
1. User logs in
2. Navigates to account page
3. Views profile information and transaction history
4. Can update email, name, or wallet key
5. Changes saved to backend

## Frontend-Backend Interactions

### Authentication
- **POST /api/auth/register**: Submit registration form
- **POST /api/auth/token**: Login with credentials
- **GET /api/auth/me**: Fetch current user profile

### Products
- **GET /api/products/**: Fetch product list for display
- **GET /api/products/{id}**: Fetch single product details

### Cart & Checkout
- Cart management handled client-side initially
- **POST /api/checkout/session**: Create payment session
- **POST /api/checkout/payment-url**: Generate Solana payment URL
- **POST /api/checkout/verify-payment**: Verify completed payment

### Account Management
- **GET /api/accounts/{username}**: Fetch account details
- **PUT /api/accounts/{username}**: Update account information

### Transactions
- **GET /api/transactions/**: Fetch user transaction history
- **GET /api/transactions/{id}**: Fetch specific transaction

## State Management
- User authentication state (JWT token in localStorage/sessionStorage)
- Shopping cart state (localStorage for persistence)
- Current user information
- Active payment session

## Security Considerations
- JWT token validation on all authenticated requests
- HTTPS required for production
- Input validation and sanitization
- CSRF protection
- Secure wallet key handling

## Planned Migration to FastUI

The frontend has been successfully rebuilt using FastUI, which provides:
- Python-based component definitions
- Automatic React rendering
- Type-safe component props with Pydantic
- Tight integration with FastAPI backend
- Reduced JavaScript complexity
- Consistent validation between frontend and backend

### FastUI Implementation

The new FastUI frontend is located at `/ui/` and provides all the functionality of the traditional template-based frontend:

#### Available Pages
1. **Homepage** (`/ui/` or `/ui/index`) - Landing page with platform features
2. **Login** (`/ui/login`) - User authentication with JWT token
3. **Register** (`/ui/register`) - New user registration
4. **Products** (`/ui/products`) - Product listing with database integration
5. **Product Detail** (`/ui/product/{id}`) - Individual product details
6. **About** (`/ui/about`) - Platform information
7. **Account** (`/ui/account`) - User profile (authenticated)
8. **Transactions** (`/ui/transactions`) - Transaction history (authenticated)
9. **Create Product** (`/ui/create-product`) - Add new products

#### Key Features
- **Dynamic Navigation**: Navbar changes based on authentication status
- **Form Validation**: Pydantic models ensure type-safe form submissions
- **Real-time Updates**: Forms submit to backend and provide immediate feedback
- **Database Integration**: Products are fetched from SQLAlchemy database
- **Authentication**: Login/register forms integrate with JWT authentication
- **Responsive Components**: Uses FastUI's built-in Bootstrap styling

### Benefits Realized
1. **Single Language**: Python for both frontend and backend ✅
2. **Type Safety**: Pydantic models ensure type consistency ✅
3. **Simplified Stack**: No separate frontend build process ✅
4. **Rapid Development**: Reuse backend models for frontend forms ✅
5. **Better Integration**: Direct API integration without manual fetch calls ✅

### Migration Status
The FastUI implementation is complete and the application has been fully switched to FastUI. All traditional template-based routes (`/`, `/login`, `/register`, etc.) now redirect to the new FastUI routes (`/ui/*`) with HTTP 302 redirects:

- `/` → `/ui/`
- `/login` → `/ui/login`
- `/register` → `/ui/register`
- `/account` → `/ui/account`
- `/about` → `/ui/about`
- `/product` → `/ui/products`

Jinja2 template rendering has been completely removed - the application is now 100% FastUI-based.
