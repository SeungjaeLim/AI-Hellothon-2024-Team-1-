from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import elders_router, questions_router, records_router, guides_router, answers_router
from app.database import Base, engine

# Initialize FastAPI app
app = FastAPI(
    title="Elderly Care Management API",
    description="API for managing records, questions, lesson plans, and preferences for elderly care",
    version="1.0.0"
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include API routers
app.include_router(elders_router, prefix="/elders", tags=["Elders"])
app.include_router(questions_router, prefix="/questions", tags=["Questions"])
app.include_router(records_router, prefix="/records", tags=["Records"])
app.include_router(guides_router, prefix="/guides", tags=["Guides"])
app.include_router(answers_router, prefix="/answers", tags=["Answers"])

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint for checking API health.
    """
    return {"message": "Elderly Care Management API is running"}
