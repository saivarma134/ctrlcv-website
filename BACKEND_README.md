# CtrlSCV Backend - Setup & Deployment Guide

## Project Structure
```
ctrlscv-website-source/
├── app.py                    # Main Flask application
├── models.py                 # Database models
├── routes.py                 # API endpoints
├── requirements.txt          # Python dependencies
├── .env.example             # Environment configuration template
├── API_DOCUMENTATION.md     # Full API documentation
├── README.md                # This file
├── index.html               # Frontend (HTML)
├── script.js                # Frontend JavaScript with API functions
└── styles.css               # Frontend styles
```

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and update any settings (especially email if you want notifications)
# nano .env  or  code .env
```

### 3. Run the Backend Server
```bash
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
* Debug mode: on
```

### 4. Test the API
Open your browser and visit:
- Health check: http://localhost:5000/api/health

Or use curl:
```bash
curl http://localhost:5000/api/health
```

### 5. Access the Frontend
Open `index.html` in your browser. The frontend JavaScript automatically connects to the backend API.

---

## Features Implemented

### 1. User Management
- User registration with email validation
- User login/authentication
- User profile management
- Role-based access (admin, customer, staff)

### 2. Contact Form Management
- Submit contact forms
- View all contacts (admin)
- Update contact status
- Automatic email notifications

### 3. Demo Requests
- Request product demos
- Schedule demo meetings
- Update demo status
- Automatic confirmation emails

### 4. Product Management
- List all products
- Filter products by category
- Create/update products (admin)
- Product details with features

### 5. Order Management
- Create orders
- Track order status
- List orders by user
- Update order status
- Order confirmation emails

---

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Check API status |
| POST | `/api/auth/register` | Register user |
| POST | `/api/auth/login` | Login user |
| POST | `/api/contact/submit` | Submit contact form |
| GET | `/api/contact/list` | Get all contacts |
| POST | `/api/demo/request` | Request demo |
| GET | `/api/demo/list` | Get all demos |
| GET | `/api/products` | List products |
| POST | `/api/products` | Create product |
| POST | `/api/orders` | Create order |
| GET | `/api/orders` | List orders |

See `API_DOCUMENTATION.md` for complete endpoint reference.

---

## Database

The application uses SQLite (file-based database):
- Database file: `ctrlscv.db`
- Tables automatically created on first run
- No additional database setup required

### Models:
- `User` - User accounts and authentication
- `Contact` - Contact form submissions
- `DemoRequest` - Demo/quote requests
- `Product` - Product/service catalog
- `Order` - Customer orders

---

## Email Configuration

To enable email notifications:

1. Set up a Gmail app password or use another SMTP provider
2. Update `.env` with your email credentials:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   ```
3. Uncomment email sending code in `routes.py` (search for `send_email` function calls)

---

## CORS Configuration

The backend allows requests from any origin by default. For production, configure CORS in `app.py`:

```python
# Change from:
CORS(app)

# To specific origins:
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": ["https://yourdomain.com"]}})
```

---

## Frontend Integration

All necessary API functions are included in `script.js`:

```javascript
// Example usage
const result = await submitContact({
  name: "John",
  email: "john@example.com",
  subject: "Inquiry",
  message: "Hello..."
});
```

Common functions available:
- `submitContact()` - Send contact form
- `submitDemoRequest()` - Request demo
- `registerUser()` - Register account
- `loginUser()` - Login
- `getProducts()` - Get products
- `createOrder()` - Create order
- `checkHealth()` - Check API status

---

## Security Considerations

For production deployment:

1. **Add Authentication** - Implement JWT tokens for API authentication
2. **Add Rate Limiting** - Prevent abuse with rate limiting middleware
3. **Use HTTPS** - Always use HTTPS in production
4. **Validate Input** - Add more robust input validation
5. **Error Handling** - Don't expose sensitive error details
6. **Environment Variables** - Keep secrets in `.env` (never commit)
7. **Database Backups** - Implement regular backups
8. **SQL Injection** - Current implementation is safe (using SQLAlchemy ORM)

---

## Production Deployment

### Using Gunicorn (recommended)

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run the app:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Using Heroku

1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Create `runtime.txt`:
   ```
   python-3.10.0
   ```

3. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(host='0.0.0.0', port=5001)  # Use different port
```

### Database Issues
```bash
# Delete the database and restart
rm ctrlscv.db
python app.py
```

### CORS Errors
Make sure the API URL in `script.js` matches your server:
```javascript
const API_URL = 'http://localhost:5000/api';
```

### Email Not Sending
- Enable "Less secure app access" in Gmail settings
- Use an app-specific password instead of your regular password
- Check SMTP settings in `.env`

---

## Development

### Hot Reload
The app runs with `debug=True` by default, enabling automatic reload on file changes.

### Database Shell
Access the database:
```bash
python
>>> from app import app, db
>>> with app.app_context():
>>>     from models import User
>>>     users = User.query.all()
```

### Clear Database
```bash
rm ctrlscv.db
python app.py
```

---

## Next Steps

1. ✅ Backend API implemented
2. ✅ Frontend JavaScript integration
3. 🔄 To Do:
   - Add JWT authentication tokens
   - Implement admin dashboard
   - Add payment processing (Stripe/PayPal)
   - Add email template engine
   - Add API documentation UI (Swagger)
   - Add unit tests
   - Set up CI/CD pipeline

---

## Support & Questions

For issues or questions, refer to:
- `API_DOCUMENTATION.md` - Full API reference
- Flask docs: https://flask.palletsprojects.com/
- SQLAlchemy docs: https://docs.sqlalchemy.org/
