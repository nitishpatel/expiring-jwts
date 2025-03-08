"""
Imported necessary models to initialize FastAPI server
"""
import logging.config
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from expiring_jwts.routes.router import router
import traceback
# Load environment variables from the .env file
load_dotenv()

# creating fastapi app
app = FastAPI()

# # Include main router
app.include_router(router)

# Configure logging using the logging.conf file
logging_conf_path = "logging.conf"
if not os.path.exists(logging_conf_path):
    print("⚠️ Warning: logging.conf file not found! Default logging will be used.")
else:
    logging.config.fileConfig(logging_conf_path)

# Use the configured logger in your FastAPI app
logger = logging.getLogger(__name__)

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException):
    """
    Handle HTTP errors raised during request processing.
    """
    if isinstance(exc.detail, dict):  # If detail is a dict (custom error structure)
        return JSONResponse(
            content={"error_code": exc.detail.get("error_code"), "message": exc.detail.get("message")},
            status_code=exc.status_code,
        )
    return JSONResponse(
        content={"message": str(exc.detail)},  # Handle normal string-based errors
        status_code=exc.status_code,
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📥 Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"📤 Response: {response.status_code}")
    return response

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Unhandled Exception: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        content={"error": "Internal Server Error", "details": str(exc)},
        status_code=500,
    )


def runserver():
    """
    Function to run FastAPI server
    """
    logger.debug("Starting FastAPI server")
    uvicorn.run("expiring_jwts.main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
