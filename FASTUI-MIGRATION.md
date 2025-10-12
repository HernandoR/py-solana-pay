# FastUI Migration Guide

## Overview
This document describes the migration from traditional HTML/CSS/JS templates to FastUI for the py-solana-pay frontend.

## What Changed

### Before (Traditional Templates)
- **Location**: `/`, `/login`, `/register`, etc.
- **Technology**: Jinja2 templates + Bootstrap + Custom JS
- **Rendering**: Server-side HTML rendering
- **State Management**: Client-side JavaScript with localStorage
- **API Calls**: Manual fetch() calls from JavaScript
- **Forms**: HTML forms with manual validation

### After (FastUI)
- **Location**: `/ui/`, `/ui/login`, `/ui/register`, etc.
- **Technology**: FastUI (Python) + React (auto-generated)
- **Rendering**: Client-side React rendering with JSON API
- **State Management**: FastUI built-in state management
- **API Calls**: Automatic via FastUI framework
- **Forms**: Pydantic models with automatic validation

## Architecture

### FastUI Request Flow
```
User Browser
    ↓
GET /ui/login (HTML page with React app)
    ↓
GET /ui/api/login (JSON components)
    ↓
POST /ui/api/login/submit (Form submission)
    ↓
Response: FireEvent with redirect/auth
    ↓
React renders new page
```

### Component Structure
Each page returns a list of FastUI components:
```python
def get_login_page() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Navbar(...),
                c.Heading(text="Login", level=1),
                c.ModelForm(model=LoginForm, ...),
                c.Link(...)
            ]
        )
    ]
```

## Available Pages

### Public Pages (No Authentication Required)
1. **Homepage** - `/ui/` or `/ui/index`
   - Hero section with platform features
   - Call-to-action buttons
   - Feature highlights

2. **Login** - `/ui/login`
   - Username/password form
   - JWT authentication
   - Redirect to account on success

3. **Register** - `/ui/register`
   - User registration form
   - Email and username validation
   - Password hashing
   - Redirect to login on success

4. **Products** - `/ui/products`
   - Product listing from database
   - View details button
   - Create new product button

5. **Product Detail** - `/ui/product/{id}`
   - Individual product information
   - Add to cart button (placeholder)

6. **About** - `/ui/about`
   - Platform information
   - Technology stack details

### Authenticated Pages (Login Required)
7. **Account** - `/ui/account`
   - User profile information
   - Account settings (placeholder)

8. **Transactions** - `/ui/transactions`
   - Transaction history (placeholder)

9. **Create Product** - `/ui/create-product`
   - Product creation form
   - Saves to database

## Form Handling

### Login Form
```python
class LoginForm(BaseModel):
    username: str = Field(title="Username")
    password: str = Field(title="Password", json_schema_extra={"type": "password"})
```

**Endpoint**: `POST /ui/api/login/submit`

**Success Response**:
```json
[
    {
        "type": "FireEvent",
        "event": {
            "type": "auth",
            "token": "eyJhbGc...",
            "url": "/ui/account"
        }
    }
]
```

**Error Response**:
```json
[
    {
        "type": "Paragraph",
        "text": "Incorrect username or password",
        "class_name": "text-danger"
    },
    {
        "type": "FireEvent",
        "event": {"type": "go-to", "url": "/ui/login"}
    }
]
```

### Registration Form
```python
class RegisterForm(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str
    fullname: str
    password: str = Field(min_length=6, json_schema_extra={"type": "password"})
    wallet_key: str = Field(default="")
```

**Endpoint**: `POST /ui/api/register/submit`

**Success**: Redirects to `/ui/login`

**Validation**:
- Username uniqueness
- Email uniqueness  
- Password minimum length (6 characters)
- Username minimum length (3 characters)

### Product Form
```python
class ProductForm(BaseModel):
    name: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    image: str = Field(default="")
```

**Endpoint**: `POST /ui/api/product/create`

**Success**: Redirects to `/ui/products`

## Navigation

The navigation bar dynamically changes based on authentication status:

### Not Authenticated
- Home
- Products
- About
- **Login** ← end link
- **Register** ← end link

### Authenticated
- Home
- Products
- About
- **Account** ← end link
- **Transactions** ← end link
- **Logout** ← end link

## Testing

### Test Registration
```bash
curl -X POST http://localhost:8000/ui/api/register/submit \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&email=test@example.com&fullname=Test User&password=password123&wallet_key="
```

### Test Login
```bash
curl -X POST http://localhost:8000/ui/api/login/submit \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

### Test Product Creation
```bash
curl -X POST http://localhost:8000/ui/api/product/create \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=My Product&price=1.0&quantity=10&image="
```

### Access Pages
```bash
# Get homepage components
curl http://localhost:8000/ui/api/index

# Get products page components
curl http://localhost:8000/ui/api/products

# Access HTML page (requires browser with internet for CDN)
curl http://localhost:8000/ui/
```

## Benefits of FastUI

### 1. Type Safety
- Forms validated with Pydantic
- Compile-time error checking
- Consistent types across frontend/backend

### 2. Simplified Development
- No separate frontend build process
- No package.json or npm dependencies
- All code in Python

### 3. Automatic Validation
- Pydantic models handle all validation
- Same validation logic on frontend and backend
- Consistent error messages

### 4. Direct Database Access
- Pages query database directly
- No need for separate API layer
- Real-time data

### 5. Reduced Boilerplate
- No manual API calls
- No state management libraries
- No routing configuration

## Migration Path

For projects currently using the traditional templates:

1. **Keep Traditional Routes**: The old routes (`/`, `/login`, etc.) still work
2. **Add FastUI Routes**: New routes at `/ui/*` path
3. **Gradual Migration**: Migrate one page at a time
4. **Deprecate Old Routes**: Once FastUI is stable, redirect old routes to new ones

## Known Limitations

1. **CDN Dependency**: FastUI requires external CDN for React components
2. **Browser Required**: API returns JSON, needs FastUI React app to render
3. **Limited Styling**: Bootstrap-based, less customizable than custom CSS
4. **Authentication State**: Currently uses AuthEvent, may need enhancement for complex auth flows

## Future Enhancements

1. **Shopping Cart**: Implement cart persistence and checkout flow
2. **Payment Integration**: Add Solana payment QR code generation
3. **Transaction Verification**: Real-time transaction status updates
4. **Admin Panel**: Product/user management interface
5. **File Uploads**: Product image uploads
6. **Advanced Authentication**: Remember me, password reset, email verification
7. **Real-time Updates**: WebSocket integration for live data
8. **Internationalization**: Multi-language support

## Troubleshooting

### Issue: Blank Page
- **Cause**: CDN blocked or no internet access
- **Solution**: Check browser console, ensure CDN access

### Issue: Form Not Submitting
- **Cause**: Validation errors
- **Solution**: Check Pydantic model constraints

### Issue: Authentication Not Working
- **Cause**: Token not stored
- **Solution**: Ensure AuthEvent is returned from login endpoint

### Issue: Products Not Loading
- **Cause**: Database empty
- **Solution**: Add sample products via API or admin interface

## Conclusion

The FastUI migration provides a modern, type-safe frontend while maintaining simplicity and tight integration with the FastAPI backend. All core functionality has been successfully migrated with improved validation and reduced complexity.
