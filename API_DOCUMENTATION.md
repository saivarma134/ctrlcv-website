# CtrlSCV Backend API Documentation

## Overview
This is the backend API for the CtrlSCV website. It provides endpoints for user authentication, contact management, demo requests, product management, and order processing.

## Base URL
```
http://localhost:5000/api
```

## Authentication
Most endpoints do not require authentication for the public-facing website. For admin endpoints, authentication tokens should be added in future implementation.

---

## Endpoints

### Health Check
- **GET** `/health`
- **Description**: Check if the API is running
- **Response**: `{ status: "healthy", timestamp: "2024-01-01T00:00:00" }`

---

## Project Routes (`/api/projects`)

### Get Project
- **GET** `/projects/<slug>`
- **Description**: Return project details for the website's View Project buttons.
- **Example**: `/projects/e-commerce-demo`
- **Response**:
  ```json
  {
    "slug": "e-commerce-demo",
    "name": "E-commerce Demo",
    "service_type": "website",
    "description": "Online store with product pages, cart and checkout."
  }
  ```

---

## Authentication Routes (`/api/auth`)

### Register User
- **POST** `/auth/register`
- **Description**: Create a new user account
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "password123",
    "full_name": "John Doe"
  }
  ```
- **Response**:
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "username",
      "full_name": "John Doe",
      "role": "customer"
    }
  }
  ```

### Login User
- **POST** `/auth/login`
- **Description**: Authenticate user credentials
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Login successful",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "username",
      "full_name": "John Doe",
      "role": "customer"
    }
  }
  ```

---

## Contact Routes (`/api/contact`)

### Submit Contact Form
- **POST** `/contact/submit`
- **Description**: Submit a contact form message
- **Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "subject": "Website Inquiry",
    "message": "I'm interested in your services..."
  }
  ```
- **Response**:
  ```json
  {
    "message": "Contact form submitted successfully",
    "contact_id": 1
  }
  ```

### Get All Contacts
- **GET** `/contact/list`
- **Description**: Get all contact submissions (admin only)
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "subject": "Website Inquiry",
      "message": "I'm interested...",
      "status": "new",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
  ```

### Get Single Contact
- **GET** `/contact/<contact_id>`
- **Description**: Get specific contact details
- **Response**: Single contact object

### Update Contact Status
- **PATCH** `/contact/<contact_id>/status`
- **Description**: Update contact status (new, read, responded)
- **Body**:
  ```json
  {
    "status": "responded"
  }
  ```

---

## Demo Request Routes (`/api/demo`)

### Request Demo
- **POST** `/demo/request`
- **Description**: Submit a demo/quote request
- **Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Acme Corp",
    "service_type": "website",
    "budget": "$5,000-$10,000",
    "timeline": "3 months",
    "description": "We need a custom website..."
  }
  ```
- **Response**:
  ```json
  {
    "message": "Demo request submitted successfully",
    "demo_id": 1
  }
  ```

### Get All Demo Requests
- **GET** `/demo/list`
- **Description**: Get all demo requests
- **Response**: Array of demo request objects

### Get Single Demo Request
- **GET** `/demo/<demo_id>`
- **Description**: Get specific demo request details

### Update Demo Request Status
- **PATCH** `/demo/<demo_id>/status`
- **Description**: Update status and schedule demo
- **Body**:
  ```json
  {
    "status": "scheduled",
    "scheduled_date": "2024-02-01T10:00:00"
  }
  ```

---

## Product Routes (`/api/products`)

### Get All Products
- **GET** `/products`
- **Description**: Get all active products
- **Query Parameters**:
  - `category` (optional): Filter by category (website, dashboard, shopos)
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Website Development",
      "slug": "website-dev",
      "description": "Modern responsive websites...",
      "category": "website",
      "price": 5000,
      "features": ["Responsive", "SEO", "CMS"],
      "is_active": true
    }
  ]
  ```

### Get Single Product
- **GET** `/products/<product_id>`
- **Description**: Get product details

### Create Product
- **POST** `/products`
- **Description**: Create new product (admin only)
- **Body**:
  ```json
  {
    "name": "Website Development",
    "slug": "website-dev",
    "description": "Modern responsive websites...",
    "category": "website",
    "price": 5000,
    "features": ["Responsive", "SEO", "CMS"]
  }
  ```

### Update Product
- **PUT** `/products/<product_id>`
- **Description**: Update product details (admin only)
- **Body**: Any of the product fields to update

---

## Order Routes (`/api/orders`)

### Create Order
- **POST** `/orders`
- **Description**: Create new order
- **Body**:
  ```json
  {
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "+1234567890",
    "product_id": 1,
    "description": "Custom requirements..."
  }
  ```
- **Response**:
  ```json
  {
    "message": "Order created successfully",
    "order": {
      "id": 1,
      "customer_name": "John Doe",
      "customer_email": "john@example.com",
      "product_id": 1,
      "amount": 5000,
      "status": "pending",
      "created_at": "2024-01-01T00:00:00"
    }
  }
  ```

### Get All Orders
- **GET** `/orders`
- **Description**: Get all orders
- **Query Parameters**:
  - `user_id` (optional): Filter by user
- **Response**: Array of order objects

### Get Single Order
- **GET** `/orders/<order_id>`
- **Description**: Get order details

### Update Order Status
- **PATCH** `/orders/<order_id>/status`
- **Description**: Update order status
- **Body**:
  ```json
  {
    "status": "confirmed"
  }
  ```
- **Status Options**: pending, confirmed, in_progress, completed, cancelled

---

## User Routes (`/api/users`)

### Get User Profile
- **GET** `/users/<user_id>`
- **Description**: Get user profile information

### Update User Profile
- **PUT** `/users/<user_id>`
- **Description**: Update user information
- **Body**:
  ```json
  {
    "full_name": "John Updated",
    "email": "newemail@example.com"
  }
  ```

---

## Frontend Integration

### Using the API in JavaScript

```javascript
// Check API health
const isHealthy = await checkHealth();

// Submit contact form
const result = await submitContact({
  name: "John",
  email: "john@example.com",
  subject: "Inquiry",
  message: "Hello..."
});

// Request demo
const demo = await submitDemoRequest({
  name: "John",
  email: "john@example.com",
  service_type: "website"
});

// Get products
const products = await getProducts();

// Create order
const order = await createOrder("John", "john@example.com", 1);

// Register user
const user = await registerUser("john@example.com", "john123", "pass", "John Doe");

// Login
const session = await loginUser("john@example.com", "pass");
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (missing or invalid fields)
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict (duplicate email, username, etc.)
- `500` - Internal Server Error

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run the Server
```bash
python app.py
```

The API will be available at `http://localhost:5000/api`

### 4. Database
SQLite database will be created automatically in the first run as `ctrlscv.db`

---

## Notes

- Email notifications are configured but disabled by default. Update SMTP settings in `routes.py` to enable.
- CORS is enabled for all origins by default. Configure as needed for production.
- Add authentication/authorization middleware for admin endpoints in production.
- Implement rate limiting for production deployment.
- Use HTTPS in production.
