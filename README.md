# Azmode Backend

Backend API for **Azmode**, an e-commerce application built with **Python, Django REST Framework, PostgreSQL and Redis**.

The backend provides RESTful APIs for authentication, product management, categories, packaging types, shopping cart, orders, inventory and user profiles.

The API is designed to communicate with the Azmode Flutter client.

---

## 🚀 Tech Stack

* **Python**
* **Django**
* **Django REST Framework**
* **PostgreSQL**
* **Redis**
* **JWT Authentication**
* **Gunicorn**
* **Nginx**
* **Git / GitHub**

---

## ✨ Features

### 🔐 Authentication & Accounts

* JWT authentication
* Access & Refresh tokens
* User profile management
* Admin and normal user roles
* Permission-based API access
* Admin-only user creation

---

### 🛍️ Products

* Create products
* Update products
* Delete products
* Retrieve product details
* Product listing
* Pagination
* Product images/media
* Category management
* Packaging type management

---

### 📂 Categories

* List categories
* Create categories
* Update categories
* Delete categories

---

### 📦 Packaging Types

* List packaging types
* Create packaging types
* Update packaging types
* Delete packaging types

---

### 🛒 Shopping Cart

* Add products to cart
* View current user's cart
* Update cart item quantity
* Remove cart items
* Select product color
* Convert cart into an order

Each user's cart is isolated from other users.

---

### 🧾 Orders

* Create orders from cart
* Store ordered products and quantities
* Track order information
* Convert cart items into orders
* Automatically decrease inventory after order creation

---

### 📊 Inventory

* Manage product stock
* Admin inventory adjustment
* Update stock through API
* Inventory changes when an order is created
* Products remain visible and purchasable even when stock is unavailable

The inventory logic intentionally allows stock to become negative according to the application's business requirements.

---

## ⚡ Redis

Redis is used as an in-memory data store to improve API performance.

Current Redis usage includes:

* API caching
* Caching frequently requested data
* Reducing unnecessary database queries
* Faster access to frequently requested resources

The architecture allows Redis to be extended for additional backend workloads in the future.

---

## 🏗️ Architecture

The production architecture follows this structure:

```text
                    ┌─────────────────┐
                    │   Flutter App   │
                    └────────┬────────┘
                             │
                           HTTPS
                             │
                             ▼
                    ┌─────────────────┐
                    │      Nginx      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Gunicorn     │
                    └────────┬────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │   Django REST API     │
                 └──────────┬────────────┘
                            │
                  ┌─────────┴─────────┐
                  │                   │
                  ▼                   ▼
          ┌──────────────┐     ┌──────────────┐
          │ PostgreSQL   │     │    Redis     │
          │   Database   │     │    Cache     │
          └──────────────┘     └──────────────┘
```

---

## 📁 Project Structure

```text
azmode-drf/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── cart/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── catalog/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── inventory/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── orders/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🔗 API Endpoints

## Authentication

```http
POST /api/account/login/
POST /api/account/refresh/
GET  /api/account/me/
```

JWT authentication is used for protected endpoints.

Example authorization header:

```http
Authorization: Bearer <access_token>
```

---

## Products

```http
GET    /api/products/
POST   /api/products/
GET    /api/products/<id>/
PUT    /api/products/<id>/
PATCH  /api/products/<id>/
DELETE /api/products/<id>/
```

Example:

```http
GET /api/products/?page=1&page_size=8
```

---

## Categories

```http
GET    /api/categories/
POST   /api/categories/
GET    /api/categories/<id>/
PUT    /api/categories/<id>/
PATCH  /api/categories/<id>/
DELETE /api/categories/<id>/
```

---

## Packaging Types

```http
GET    /api/packaging-types/
POST   /api/packaging-types/
GET    /api/packaging-types/<id>/
PUT    /api/packaging-types/<id>/
PATCH  /api/packaging-types/<id>/
DELETE /api/packaging-types/<id>/
```

---

## Cart

```http
GET    /api/cart/
POST   /api/cart/add/
PUT    /api/cart/<id>/
PATCH  /api/cart/<id>/
DELETE /api/cart/<id>/
```

Example request:

```json
{
    "product": 1,
    "quantity": 2,
    "selected_color": "white"
}
```

---

## Orders

```http
GET  /api/orders/
POST /api/orders/
```

Creating an order converts the user's cart into an order and updates product inventory.

---

## Inventory

```http
POST /api/inventory/<productId>/adjust/
```

Example request:

```json
{
    "new_stock": 25
}
```

Inventory management is restricted to authorized administrative users.

---

# 🔐 Permissions

The API separates normal users from administrators.

### 👤 Normal User

A normal user can:

* Authenticate
* View products
* View categories
* View packaging types
* Manage their own cart
* Create orders
* View their own orders
* View and manage their profile

### 👑 Admin

Administrators can additionally:

* Create users
* Manage products
* Manage categories
* Manage packaging types
* Manage inventory
* Access administrative functionality

---

# 🗄️ Database

The production database is **PostgreSQL**.

Main data domains include:

```text
Users
Products
Categories
Packaging Types
Cart Items
Orders
Inventory
```

PostgreSQL is used as the primary persistent database, while Redis is used for high-speed in-memory operations such as caching.

---

# ⚙️ Environment Variables

Create a `.env` file for local development.

Example:

```env
DEBUG=False

SECRET_KEY=your-secret-key

DB_NAME=azmode
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/1
```

> Never commit `.env` files or secret credentials to GitHub.

---

# 🧪 Local Development

## 1. Clone the repository

```bash
git clone https://github.com/mehrdadfbx/azmode-drf.git
cd azmode-drf
```

---

## 2. Create a virtual environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create your `.env` file and configure:

```text
Django
PostgreSQL
Redis
```

---

## 5. Run migrations

```bash
python manage.py migrate
```

---

## 6. Create an admin user

```bash
python manage.py createsuperuser
```

---

## 7. Start Redis

Make sure Redis is running locally.

Example:

```bash
redis-server
```

Check Redis:

```bash
redis-cli ping
```

Expected response:

```text
PONG
```

---

## 8. Run Django

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

# 🧪 API Testing

The API can be tested using:

* Postman
* Insomnia
* cURL
* Flutter application

Example:

```bash
curl http://127.0.0.1:8000/api/products/
```

For authenticated endpoints:

```bash
curl \
  -H "Authorization: Bearer <access_token>" \
  http://127.0.0.1:8000/api/account/me/
```

---

# 📱 Flutter Integration

Azmode Backend provides the REST API consumed by the Azmode Flutter application.

The Flutter application communicates with the backend for:

```text
Authentication
       │
       ├── Products
       │
       ├── Categories
       │
       ├── Packaging Types
       │
       ├── Cart
       │
       ├── Orders
       │
       ├── Inventory
       │
       └── User Profile
```

This separation allows the mobile client and backend to evolve independently.

---

# 🌐 Production Deployment

The backend is designed to run in a Linux production environment using:

```text
Ubuntu
   │
   ▼
Nginx
   │
   ▼
Gunicorn
   │
   ▼
Django REST Framework
   │
   ├──────────────► PostgreSQL
   │
   └──────────────► Redis
```

### Production components

* Ubuntu Server
* Nginx
* Gunicorn
* PostgreSQL
* Redis
* Django
* Django REST Framework

Nginx handles incoming HTTP/HTTPS requests and forwards application traffic to Gunicorn.

Gunicorn runs the Django application using multiple workers.

PostgreSQL stores persistent application data.

Redis provides high-speed in-memory data access and caching.

---

# 🔄 Development Workflow

The project uses Git for version control.

Typical workflow:

```bash
git pull

git checkout -b feature/new-feature

# Make changes

git add .

git commit -m "Add new feature"

git push origin feature/new-feature
```

---

# 🔒 Security Considerations

The project follows common backend security practices including:

* Environment-based secrets
* JWT authentication
* Permission-based access control
* Protected administrative endpoints
* HTTPS in production
* PostgreSQL instead of local SQLite in production
* Secret credentials excluded from Git

---

# 📈 Future Improvements

Possible future improvements include:

* Background task processing with Celery
* Scheduled tasks
* More advanced Redis caching
* API documentation with OpenAPI / Swagger
* Automated tests
* CI/CD pipeline
* Improved monitoring and logging

---

# 🎯 Project Goals

Azmode Backend was built to provide a maintainable REST API for a real-world e-commerce application.

The project focuses on:

* REST API design
* Authentication & authorization
* Database modeling
* PostgreSQL
* Redis caching
* Inventory management
* Shopping cart logic
* Order processing
* Production deployment
* Flutter API integration

---

# 👨‍💻 Author

**Mehrdad**

Danyal

Python & Django Backend Developer

GitHub:

https://github.com/mehrdadfbx
