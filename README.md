# MediGen Pharmaceuticals - Full-Stack Application

A modern pharmaceutical e-commerce platform with Flask API backend and React frontend, featuring JWT authentication, MySQL database, and comprehensive product management.

## 📚 Documentation

For complete API documentation, integration guides, setup instructions, and examples:

**[→ View Complete Documentation](docs-index.html)**

Open `docs-index.html` in your browser to access:
- Backend API Documentation (all endpoints with examples)
- Frontend Integration Guide (React components and patterns)
- Quick Start Guide with setup commands
- Test credentials and authentication details
- Technology stack overview

## � Project Structure

```
medigen-interview/
│
├── backend/                      # Flask REST API Backend
│   ├── app/
│   │   ├── __init__.py          # Flask app initialization
│   │   ├── models.py            # SQLAlchemy database models
│   │   └── routes.py            # API endpoint definitions
│   │
│   ├── config.py                # Configuration settings
│   ├── run.py                   # Application entry point
│   ├── seed.py                  # Database seeding script
│   ├── requirements.txt         # Python dependencies
│   └── docs.html               # Backend API documentation
│
├── frontend/                     # React Frontend Application
│   ├── public/
│   │   ├── index.html           # HTML template
│   │   └── manifest.json        # PWA configuration
│   │
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Auth/
│   │   │   │   ├── Login.js     # Login component
│   │   │   │   └── Login.css    # Login styles
│   │   │   │
│   │   │   ├── product/
│   │   │   │   ├── ProductInfo.js    # Product details
│   │   │   │   └── Substitutes.js    # Product alternatives
│   │   │   │
│   │   │   ├── ProductPage.js   # Main product page
│   │   │   └── ProductPage.css  # Product page styles
│   │   │
│   │   ├── services/
│   │   │   └── api.js           # API service layer
│   │   │
│   │   ├── App.js               # Root component & routing
│   │   ├── App.css              # Global application styles
│   │   ├── index.js             # React DOM entry point
│   │   └── index.css            # Global CSS
│   │
│   ├── package.json             # Node dependencies
│   └── docs.html               # Frontend integration guide
│
└── docs-index.html              # Documentation hub (START HERE)
```

## 🗄️ Database Structure

The application uses MySQL with 11 normalized tables:

### Core Entities
- **users** - User accounts with bcrypt-hashed passwords
- **products** - Main product catalog with details
- **manufacturers** - Pharmaceutical companies
- **categories** - Product categorization
- **salts** - Active pharmaceutical ingredients

### Relationships
- **product_salts** - Many-to-many: Products ↔ Salts
- **substitutes** - Product alternatives
- **faqs** - Product frequently asked questions
- **reviews** - User reviews with ratings
- **orders** - Order information
- **order_items** - Order line items

## 🎯 Key Features

### Backend (Flask)
- RESTful API with 15+ endpoints
- JWT authentication with refresh tokens
- SQLAlchemy ORM with normalized schema
- CORS enabled for frontend integration
- Comprehensive error handling

### Frontend (React)
- Modern component-based architecture
- React Router for client-side routing
- API service layer for clean separation
- JWT token management
- Responsive design with gradients

## 🚀 Quick Start

1. **View Documentation**: Open `docs-index.html` in your browser
2. **Setup Database**: Create MySQL database `medigen_db`
3. **Backend**: Navigate to `backend/`, activate venv, run `python seed.py` then `python run.py`
4. **Frontend**: Navigate to `frontend/`, run `npm install` then `npm start`
5. **Login**: Use test credentials from documentation

## � Test Credentials

See `docs-index.html` for complete list of test accounts with passwords.

---

**For detailed setup, API reference, and integration examples, open [docs-index.html](docs-index.html) in your browser.**