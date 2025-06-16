# MercadoLibre Clone - E-commerce Platform

## Overview

This is a Flask-based e-commerce web application inspired by MercadoLibre, featuring product browsing, search functionality, and shopping cart capabilities. The application is built with a modern tech stack focusing on simplicity and user experience.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **UI Framework**: Bootstrap 5.3.0 for responsive design
- **Icons**: Font Awesome 6.4.0
- **Styling**: Custom CSS with MercadoLibre-inspired color scheme
- **JavaScript**: Vanilla JavaScript for interactive features

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Session Management**: Flask sessions with secret key configuration
- **Data Storage**: JSON file-based product catalog
- **Server**: Gunicorn WSGI server for production deployment

### Application Structure
- `app.py`: Main Flask application with routes and business logic
- `main.py`: Application entry point for development
- `templates/`: HTML templates for rendering pages
- `static/`: CSS, JavaScript, and static assets
- `data/`: JSON data files for product information

## Key Components

### Core Routes
- **Home Route (`/`)**: Product listing with search and category filtering
- **Product Detail (`/product/<id>`)**: Individual product pages
- **Cart Management (`/add_to_cart`)**: Shopping cart functionality (incomplete)

### Data Management
- **Product Catalog**: JSON-based product storage with fields for:
  - ID, name, description, price
  - Category, image URL, stock, rating
- **Session Storage**: Cart data stored in Flask sessions

### User Interface
- **Responsive Design**: Mobile-first Bootstrap implementation
- **Search Functionality**: Real-time product search by name/description
- **Category Filtering**: Product filtering by categories
- **Product Cards**: Grid-based product display with images and pricing

## Data Flow

1. **Product Loading**: JSON data loaded from `data/products.json` on each request
2. **Search/Filter**: Query parameters processed to filter product list
3. **Template Rendering**: Filtered products passed to Jinja2 templates
4. **Client Interaction**: JavaScript handles UI interactions and form submissions
5. **Session Management**: Cart data persisted in Flask sessions

## External Dependencies

### Python Packages
- `flask>=3.1.1`: Web framework
- `flask-sqlalchemy>=3.1.1`: Database ORM (installed but not used)
- `psycopg2-binary>=2.9.10`: PostgreSQL adapter (installed but not used)
- `gunicorn>=23.0.0`: Production WSGI server
- `email-validator>=2.2.0`: Email validation utilities

### Frontend Dependencies (CDN)
- Bootstrap 5.3.0: UI framework
- Font Awesome 6.4.0: Icon library

### Infrastructure
- PostgreSQL: Database system (configured but not implemented)
- OpenSSL: Security library

## Deployment Strategy

### Development Environment
- **Server**: Flask development server on port 5000
- **Configuration**: Debug mode enabled, hot reload
- **Host**: Bound to all interfaces (0.0.0.0)

### Production Environment
- **Server**: Gunicorn with autoscale deployment target
- **Configuration**: Multi-worker setup with port reuse
- **Platform**: Replit deployment with Nix package management

### Environment Configuration
- Session secret key configurable via environment variable
- Development fallback for session secret
- PostgreSQL packages pre-installed for future database integration

## Changelog
- June 16, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.

## Notes for Development

### Current Limitations
- Shopping cart functionality is incomplete (add_to_cart route not finished)
- No user authentication system implemented
- Database integration prepared but not active (using JSON files)
- No order processing or payment integration

### Future Enhancement Areas
- Complete shopping cart implementation
- User registration and authentication
- Database migration from JSON to PostgreSQL
- Order management system
- Payment gateway integration
- Admin panel for product management