# Import necessary modules

import uvicorn
from fastapi import APIRouter, FastAPI
from starlette.config import Config
from routers import video_catalog
from src.api.schemas import ErrorResponse



# Load configuration

config = Config(".env")
ENVIRONMENT = config("ENVIRONMENT")  # Get current environment name
SHOW_DOCS_ENVIRONMENT = ("local", "STAGING")

# Create FastAPI application instance

router = APIRouter()

# Swagger Configuration
app_configs = {
    "title": "Video Catalog API",
    "version": "0.1.0",
    "description": "A platform that allows Create, Read, Update, Delete Video.",
}

# Define application configurations
app = FastAPI(
    **app_configs,
    responses={
        422: {
            "description": "Validation Error",
            "model": ErrorResponse,
        },
    }
)
# Include routers

app.include_router(video_catalog.router)


# Run the application

def run_application():
    """
    Run the FastAPI application.

    This function starts the UVicorn server and runs the FastAPI application.

    Returns:
        None
    """
    uvicorn.run(app, host="localhost", port=8000, log_level="info")


if __name__ == "__main__":
    run_application()
