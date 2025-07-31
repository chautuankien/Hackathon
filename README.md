# Authentication Service

A microservice-based authentication system built with FastAPI that provides secure login functionality with email/password authentication, JWT token management, and user registration.

## 🚀 Features

- **User Registration**: Create new user accounts with email validation
- **Email/Password Login**: Secure authentication with bcrypt password hashing
- **JWT Token Management**: Access tokens (30 min) and refresh tokens (7 days)
- **Token Validation**: Middleware for protecting API endpoints
- **Session Management**: Automatic token refresh and logout functionality
- **Microservice Architecture**: Designed for easy integration with other services
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## 📁 Project Structure

```
auth-service/
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py              # Cấu hình
│   ├── api/v1/                # API endpoints
│   ├── core/                  # Security & exceptions
│   ├── services/              # Business logic
│   ├── models/                # Database models
│   ├── schemas/               # Pydantic schemas
│   ├── database/              # DB connection
│   └── repositories/          # Data access layer
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── USAGE.md
```

## 🏗️ Architecture Explanation

### **Layered Architecture**

The project follows a clean architecture pattern with clear separation of concerns:

#### **1. API Layer (`app/api/`)**
- **Purpose**: Handle HTTP requests and responses
- **Responsibilities**: Route definition, request validation, response formatting
- **Files**: `auth.py` contains all authentication endpoints

#### **2. Service Layer (`app/services/`)**
- **Purpose**: Business logic and orchestration
- **Responsibilities**: Coordinate between repositories, implement business rules
- **Files**: `auth_service.py` handles authentication workflows

#### **3. Repository Layer (`app/repositories/`)**
- **Purpose**: Data access abstraction
- **Responsibilities**: Database operations, query construction
- **Files**: `user_repository.py` handles user CRUD operations

#### **4. Core Layer (`app/core/`)**
- **Purpose**: Shared utilities and infrastructure
- **Responsibilities**: Security functions, custom exceptions
- **Files**: `security.py` for JWT/password, `exceptions.py` for error handling

#### **5. Models (`app/models/`)**
- **Purpose**: Database schema definition
- **Responsibilities**: SQLAlchemy models, table relationships
- **Files**: `user.py` defines user table structure

#### **6. Schemas (`app/schemas/`)**
- **Purpose**: Data validation and serialization
- **Responsibilities**: Pydantic models for API input/output
- **Files**: Request/response validation schemas

### **Microservice Design Benefits**

- **Independence**: Can run standalone without external dependencies
- **Scalability**: Easy to scale authentication service separately
- **Maintainability**: Clear boundaries and single responsibility
- **Extensibility**: Easy to add new features (corporate login, 2FA, etc.)
- **Testability**: Each layer can be tested independently

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Poetry (Python dependency manager)

### 1. Clone Repository

```bash
git clone <repository-url>
cd auth-service
```

### 2. Install Dependencies with Poetry

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Activate virtual environment
poetry shell
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
DATABASE_URL=postgresql://username:password@localhost:5432/auth_db
SECRET_KEY=your-super-secret-key-change-in-production-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 4. Database Setup

```bash
# Start PostgreSQL container
docker-compose up -d db

# Check if database is running
docker-compose ps
```

### 5. Run the Application

```bash
# Development mode with auto-reload
poetry run uvicorn app.main:app --reload --port 8000

# Or activate shell first
poetry shell
python -m app.main
```

The service will be available at: http://localhost:8000

## 📚 API Documentation

Once the service is running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Login Email/Password Feature Usage

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | User login |
| GET | `/api/v1/auth/me` | Get current user info |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| POST | `/api/v1/auth/logout` | User logout |
| GET | `/api/v1/auth/validate-token` | Validate token (for services) |

### 1. User Registration

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "SecurePass123",
       "full_name": "John Doe"
     }'
```

**Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "created_at": "2025-07-31T10:00:00Z"
  }
}
```

### 2. User Login

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "SecurePass123"
     }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
      "id": 1,
      "email": "user@example.com",
      "full_name": "John Doe",
      "is_active": true,
      "is_corporate": false,
      "created_at": "2025-07-31T10:00:00Z"
    }
  }
}
```

### 3. Access Protected Endpoints

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer <access_token>"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_corporate": false,
    "created_at": "2025-07-31T10:00:00Z"
  }
}
```

### 4. Token Refresh

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
     -H "Content-Type: application/json" \
     -d '{
       "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
     }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Token refreshed successfully",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```