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


# Load environment variables from the .env file
load_dotenv()

# creating fastapi app
app = FastAPI()

# # Include main router
# app.include_router(router)

# Configure logging using the logging.conf file
logging.config.fileConfig("logging.conf")

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
    return JSONResponse(
        content={"error_code": exc.detail.get("error_code"), "message": exc.detail.get("message")},
        status_code=exc.status_code,
    )


def runserver():
    """
    Function to run FastAPI server
    """
    logger.debug("Starting FastAPI server")
    uvicorn.run("expiring_jwts.main:app", host="0.0.0.0", port=8000, reload=True)
