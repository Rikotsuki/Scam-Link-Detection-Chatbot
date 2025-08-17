#!/usr/bin/env python3
"""
Startup script for PhishGuard Python API service
"""
import uvicorn
import os
from app.api import app

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv("PYTHON_SERVICE_PORT", 8000))
    host = os.getenv("PYTHON_SERVICE_HOST", "0.0.0.0")
    
    print(f"Starting PhishGuard Python API service on {host}:{port}")
    print("API Documentation available at:")
    print(f"  - Swagger UI: http://{host}:{port}/docs")
    print(f"  - ReDoc: http://{host}:{port}/redoc")
    
    uvicorn.run(
        "app.api:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    ) 