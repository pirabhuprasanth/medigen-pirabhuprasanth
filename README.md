# MediGen Pharmaceuticals - Full-Stack Application

A modern pharmaceutical e-commerce platform with Flask API backend and React frontend, featuring JWT authentication, MySQL database, and comprehensive product management.

## 📚 Documentation

- **[Backend API Documentation](backend/docs.html)** - Complete API reference with all endpoints, request/response examples, and integration guides
- **[Frontend Integration Guide](frontend/docs.html)** - React component examples, API service layer, authentication flow, and best practices

## 🏗️ Architecture Overview

- **Backend**: Flask API with SQLAlchemy ORM, JWT authentication, MySQL database
- **Frontend**: React.js with modern UI components, routing, and authentication
- **Database**: Normalized MySQL schema with 11+ tables for comprehensive product management
- **Authentication**: JWT-based authentication with refresh tokens

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- MySQL 8.0 or higher
- npm or yarn package manager

## 🛠️ Project Setup

### 1. Clone and Navigate
```bash
git clone [your-repo-url]
cd medigen-interview
```

### 2. Database Setup

#### Install MySQL
- Windows: Download from [MySQL Official Site](https://dev.mysql.com/downloads/mysql/)
- macOS: `brew install mysql`
- Linux: `sudo apt-get install mysql-server`

#### Create Database
```sql
-- Login to MySQL as root
mysql -u root -p

-- Create database and user
CREATE DATABASE medigen_db;
CREATE USER 'medigen_user'@'localhost' IDENTIFIED BY 'medigen_password';
GRANT ALL PRIVILEGES ON medigen_db.* TO 'medigen_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (create .env file)
echo "FLASK_ENV=development" > .env
echo "DATABASE_URL=mysql://medigen_user:medigen_password@localhost/medigen_db" >> .env
echo "JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production" >> .env

# Initialize database and seed data
python seed.py

# Run Flask server
python run.py
```

Backend will be available at: `http://localhost:5000`

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start React development server
npm start
```

Frontend will be available at: `http://localhost:3000`

## 🔐 Demo Accounts

### Admin User
- **Email**: admin@medigen.com
- **Password**: admin123
- **Role**: Administrator

### Regular Users
- **Email**: doctor@medigen.com
- **Password**: doctor123
- **Role**: Doctor

- **Email**: patient@medigen.com
- **Password**: patient123
- **Role**: Patient

## 🌟 Features

### Backend API Features
- **Authentication**
  - JWT-based login/logout with refresh tokens
  - User registration and profile management
  - Role-based access control

- **Product Management**
  - Comprehensive product catalog with detailed information
  - Salt composition tracking
  - Manufacturer and category management
  - Product search and filtering

- **Review System**
  - User reviews and ratings
  - Review aggregation and statistics

- **Order Management**
  - Order creation and tracking
  - Order history for users

### Frontend Features
- **Modern UI**
  - Professional pharmaceutical e-commerce design
  - Responsive layout for all devices
  - Gradient backgrounds and smooth animations

- **Authentication**
  - Secure login with error handling
  - Demo account quick access
  - Automatic token management

- **Navigation**
  - React Router for seamless navigation
  - Protected routes for authenticated users
  - User-friendly logout functionality

## 📚 API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration  
- `POST /api/logout` - User logout
- `POST /api/refresh` - Refresh JWT token
- `GET /api/profile` - Get user profile

### Products
- `GET /api/products` - Get all products (paginated)
- `GET /api/product/{id}` - Get specific product details
- `GET /api/search?q={query}` - Search products
- `GET /api/categories` - Get all categories
- `GET /api/manufacturers` - Get all manufacturers

### Reviews
- `GET /api/product/{id}/reviews` - Get product reviews
- `POST /api/product/{id}/reviews` - Add product review

### Orders
- `GET /api/orders` - Get user orders
- `POST /api/orders` - Create new order

## 🗄️ Database Schema

### Core Tables
- **users** - User accounts and authentication
- **manufacturers** - Pharmaceutical companies
- **categories** - Product categories
- **products** - Main product information
- **salts** - Active pharmaceutical ingredients
- **product_salts** - Many-to-many relationship for product compositions
- **substitutes** - Alternative medicines
- **faqs** - Product frequently asked questions
- **reviews** - User reviews and ratings
- **orders** - Order information
- **order_items** - Order line items

## 🛡️ Security Features

- **JWT Authentication** with secure token handling
- **Password Hashing** using bcrypt
- **CORS Protection** configured for frontend integration
- **SQL Injection Protection** through SQLAlchemy ORM
- **Input Validation** on all API endpoints

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🚀 Production Deployment

### Backend Production Setup
1. Set `FLASK_ENV=production` in environment variables
2. Use production-grade WSGI server like Gunicorn
3. Configure MySQL for production with proper credentials
4. Set strong JWT secret key
5. Enable HTTPS

### Frontend Production Build
```bash
cd frontend
npm run build
```

## 📝 Environment Variables

### Backend (.env)
```
FLASK_ENV=development
DATABASE_URL=mysql://medigen_user:medigen_password@localhost/medigen_db
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
```

## 🎯 Key Technologies

### Backend Stack
- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing
- **bcrypt** - Password hashing
- **MySQL** - Relational database

### Frontend Stack
- **React** - Modern JavaScript UI library
- **React Router** - Client-side routing
- **Modern CSS** - Gradients, animations, responsive design
- **Fetch API** - HTTP client for API calls

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify MySQL is running
   - Check database credentials in .env file
   - Ensure database and user exist

2. **JWT Token Errors**
   - Check JWT_SECRET_KEY is set
   - Verify token expiration settings
   - Clear browser localStorage if needed

3. **CORS Errors**
   - Ensure Flask CORS is properly configured
   - Check frontend API base URL matches backend

4. **React Router Not Working**
   - Verify react-router-dom is installed
   - Check routing configuration in App.js

## 📞 Support

For technical support or questions about the implementation, please refer to the comprehensive code documentation within each component and API endpoint.

## 🏃‍♂️ Quick Start

1. **Setup Database**: Create MySQL database and user
2. **Start Backend**: `cd backend && python run.py`
3. **Start Frontend**: `cd frontend && npm start`
4. **Login**: Use demo credentials at `http://localhost:3000`

The system is now ready for development and testing!