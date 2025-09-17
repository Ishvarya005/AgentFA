"""
Example FastAPI application demonstrating the authentication system.
"""
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.middleware.auth_middleware import get_current_user, require_role, require_any_role
from core.models.auth_models import TokenPayload
from api.auth import router as auth_router
from core.config import config_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Faculty Advisor Authentication System",
    description="Authentication and session management for the Faculty Advisor Agentic System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication router
app.include_router(auth_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Faculty Advisor Authentication System",
        "version": "1.0.0",
        "endpoints": {
            "login": "/auth/login",
            "logout": "/auth/logout",
            "user_info": "/auth/me",
            "session_status": "/auth/session/status",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test Redis connection
        config = config_manager.load_config()
        import redis
        redis_client = redis.Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.database,
            password=config.redis.password if config.redis.password else None
        )
        redis_client.ping()
        
        return {
            "status": "healthy",
            "services": {
                "redis": "connected",
                "authentication": "available"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@app.get("/protected")
async def protected_endpoint(current_user: TokenPayload = Depends(get_current_user)):
    """Example protected endpoint requiring authentication."""
    return {
        "message": "This is a protected endpoint",
        "user": {
            "user_id": current_user.sub,
            "email": current_user.email,
            "role": current_user.role,
            "session_id": current_user.session_id
        }
    }


@app.get("/admin-only")
async def admin_only_endpoint(current_user: TokenPayload = Depends(require_role("admin"))):
    """Example endpoint requiring admin role."""
    return {
        "message": "Admin access granted",
        "user": {
            "user_id": current_user.sub,
            "email": current_user.email,
            "role": current_user.role
        }
    }


@app.get("/faculty-or-admin")
async def faculty_or_admin_endpoint(
    current_user: TokenPayload = Depends(require_any_role("faculty", "admin"))
):
    """Example endpoint requiring faculty or admin role."""
    return {
        "message": "Faculty or admin access granted",
        "user": {
            "user_id": current_user.sub,
            "email": current_user.email,
            "role": current_user.role
        }
    }


@app.get("/student-data")
async def get_student_data(current_user: TokenPayload = Depends(get_current_user)):
    """Example endpoint that returns different data based on user role."""
    if current_user.role == "student":
        # Students can only see their own data
        return {
            "message": "Your student data",
            "data": {
                "student_id": current_user.sub,
                "email": current_user.email,
                "cgpa": 8.5,
                "semester": 6,
                "backlogs": 0
            }
        }
    elif current_user.role in ["faculty", "admin"]:
        # Faculty and admin can see aggregated data
        return {
            "message": "Student data overview",
            "data": {
                "total_students": 150,
                "average_cgpa": 7.8,
                "students_with_backlogs": 25,
                "current_semester": 6
            }
        }
    else:
        raise HTTPException(status_code=403, detail="Access denied")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "example_auth_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )