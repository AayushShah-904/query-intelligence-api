from fastapi import FastAPI
from app.config import settings
from app.database import init_db
from app.routers import queries

# Initialise the FastAPI application instance with project metadata
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Ensure database tables exist before accepting API requests
init_db()

# Register query intelligence endpoints
app.include_router(queries.router)
