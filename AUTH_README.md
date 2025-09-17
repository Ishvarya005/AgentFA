# Authentication and Session Management System

This document describes the authentication and session management system implemented for the Faculty Advisor Agentic System.

## Overview

The authentication system provides secure access control with JWT-based authentication and Redis-backed session management. It ensures that only authorized users with `@amrita.edu` email addresses can access the system, with complete session isolation between users.

## Features

### ✅ Implemented Features

1. **Email Domain Validation**: Only `@amrita.edu` email addresses are allowed
2. **JWT-based Authentication**: Secure token-based authentication with configurable expiration
3. **Redis Session Management**: Fast, scalable session storage with automatic expiration
4. **User Session Isolation**: Complete isolation of user data and state
5. **Role-based Access Control**: Support for student, faculty, and admin roles
6. **Session State Management**: Persistent conversation history, agent contexts, and user preferences
7. **Workflow Management**: Support for multi-step workflows (e.g., leave applications)
8. **Comprehensive Error Handling**: Proper error classification and responses
9. **FastAPI Integration**: Ready-to-use middleware and dependencies
10. **Unit Tests**: Comprehensive test coverage for all components

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Authentication System                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Authentication  │  │ Session Manager │  │ Middleware  │ │
│  │    Service      │  │                 │  │             │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   JWT Tokens    │  │  Redis Storage  │  │ User State  │ │
│  │                 │  │                 │  │   Spaces    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Data Models

- **LoginRequest/LoginResponse**: Authentication request/response models
- **TokenPayload**: JWT token structure with user information
- **SessionData**: Redis-stored session information
- **User**: User profile information
- **UserRole**: Enum for user roles (student, faculty, admin)

## Usage

### 1. Basic Authentication

```python
from core.services.auth_service import AuthenticationService
from core.models.auth_models import LoginRequest
from core.config import config_manager

# Initialize service
config = config_manager.load_config()
auth_service = AuthenticationService(config)

# Authenticate user
login_request = LoginRequest(
    email="student@amrita.edu",
    password="password123"
)

login_response = await auth_service.authenticate_user(login_request)
print(f"Access token: {login_response.access_token}")
print(f"User role: {login_response.role}")
```

### 2. Session Management

```python
from core.services.session_manager import SessionManager

# Initialize session manager
session_manager = SessionManager(config)

# Create user state space
state_space = await session_manager.create_user_state_space(
    user_id="user123",
    session_id="session456"
)

# Add conversation message
await session_manager.add_conversation_message(
    user_id="user123",
    session_id="session456",
    agent_type="solution_advisory",
    message={
        "type": "user_query",
        "content": "How can I clear my backlogs?",
        "metadata": {"source": "web_ui"}
    }
)

# Get conversation history
history = await session_manager.get_conversation_history(
    user_id="user123",
    session_id="session456",
    limit=10
)
```

### 3. FastAPI Integration

```python
from fastapi import FastAPI, Depends
from core.middleware.auth_middleware import get_current_user, require_role
from core.models.auth_models import TokenPayload
from api.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)

@app.get("/protected")
async def protected_endpoint(current_user: TokenPayload = Depends(get_current_user)):
    return {"message": f"Hello {current_user.email}"}

@app.get("/admin-only")
async def admin_endpoint(current_user: TokenPayload = Depends(require_role("admin"))):
    return {"message": "Admin access granted"}
```

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/auth/login` | User login | None |
| POST | `/auth/logout` | User logout | Required |
| POST | `/auth/refresh` | Refresh session | Required |
| GET | `/auth/me` | Get user info | Required |
| GET | `/auth/session/status` | Get session status | Required |
| DELETE | `/auth/session/clear` | Clear session data | Required |

### Example Requests

#### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@amrita.edu",
    "password": "password123"
  }'
```

#### Access Protected Endpoint
```bash
curl -X GET "http://localhost:8000/protected" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Configuration

### Environment Variables

```bash
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# JWT Configuration
SECRET_KEY=your-secret-key-here
SESSION_TIMEOUT_MINUTES=60

# Email Domain Validation
ALLOWED_EMAIL_DOMAINS=amrita.edu
```

### Configuration File (config.yaml)

```yaml
environment: development
debug: true
secret_key: "your-secret-key-here"
session_timeout_minutes: 60
allowed_email_domains:
  - "amrita.edu"

redis:
  host: localhost
  port: 6379
  database: 0
  password: ""
  max_connections: 10
```

## Security Features

### 1. Email Domain Validation
- Only `@amrita.edu` email addresses are accepted
- Validation occurs at both Pydantic model level and service level

### 2. JWT Token Security
- Configurable secret key
- Token expiration enforcement
- Secure token generation and validation

### 3. Session Security
- Redis-based session storage with TTL
- Session isolation between users
- Automatic session cleanup

### 4. Role-based Access Control
- Support for multiple user roles
- Flexible role requirements (single role or multiple roles)
- Automatic role detection from email patterns

## User Roles

The system automatically detects user roles based on email patterns:

| Email Pattern | Role | Example |
|---------------|------|---------|
| `*@amrita.edu` | student | `john.doe@amrita.edu` |
| `faculty.*@amrita.edu` | faculty | `faculty.smith@amrita.edu` |
| `prof.*@amrita.edu` | faculty | `prof.johnson@amrita.edu` |
| `admin.*@amrita.edu` | admin | `admin.user@amrita.edu` |

## Session State Management

Each user session maintains:

- **Conversation History**: Messages exchanged with agents
- **Agent Contexts**: Per-agent state and context information
- **User Preferences**: User-specific settings and preferences
- **Active Workflows**: Multi-step processes (e.g., leave applications)
- **Cached Data**: Temporary data for performance optimization

## Error Handling

The system provides comprehensive error handling:

- **AuthenticationError**: Base authentication error
- **SessionExpiredError**: Session has expired
- **UnauthorizedError**: Invalid credentials or permissions
- **InvalidTokenError**: Malformed or invalid JWT token

## Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run authentication service tests
python -m pytest tests/test_auth_service.py -v

# Run session manager tests
python -m pytest tests/test_session_manager.py -v

# Run middleware tests
python -m pytest tests/test_auth_middleware.py -v

# Run API tests
python -m pytest tests/test_auth_api.py -v

# Run all authentication tests
python -m pytest tests/test_auth*.py -v
```

### Manual Testing

```bash
# Run the comprehensive test script
python test_auth_system.py

# Run the example application
python example_auth_app.py
```

## Dependencies

```
fastapi
uvicorn
pydantic
PyJWT
redis
python-multipart
email-validator
pytest
pytest-asyncio
httpx
```

## Production Considerations

### 1. Security
- Use strong, randomly generated secret keys
- Enable Redis authentication and encryption
- Use HTTPS in production
- Implement rate limiting for authentication endpoints

### 2. Scalability
- Configure Redis clustering for high availability
- Use connection pooling for Redis connections
- Implement horizontal scaling for multiple application instances

### 3. Monitoring
- Monitor authentication success/failure rates
- Track session creation and expiration
- Set up alerts for suspicious authentication patterns

### 4. Configuration
- Use environment variables for sensitive configuration
- Implement configuration validation
- Use different configurations for different environments

## Integration with University Systems

For production deployment, the authentication system can be integrated with:

- **LDAP/Active Directory**: For user authentication
- **University Database**: For user profile information
- **Single Sign-On (SSO)**: For seamless authentication
- **Email Systems**: For notifications and communications

## Future Enhancements

- [ ] Multi-factor authentication (MFA)
- [ ] OAuth2/OpenID Connect integration
- [ ] Audit logging for security compliance
- [ ] Password reset functionality
- [ ] Account lockout policies
- [ ] Session analytics and reporting

## Support

For questions or issues related to the authentication system, please refer to:

1. This documentation
2. Unit tests for usage examples
3. Example application for integration patterns
4. Configuration files for setup guidance