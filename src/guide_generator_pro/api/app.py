from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict
import uuid
from pathlib import Path

from ..flow import GuideGeneratorFlow
from ..database.manager import DatabaseManager
from ..utils.logger import setup_logger

# Setup
app = FastAPI(
    title="AI Guide Generator API",
    description="Generate beginner-friendly guides from multiple sources",
    version="1.0.0"
)

logger = setup_logger("api")
db = DatabaseManager()

# In-memory task storage (use Redis in production)
task_status: Dict[str, dict] = {}


class GenerateGuideRequest(BaseModel):
    """Request model for guide generation"""
    youtube_links: str = ""
    webpage_links: str = ""
    research_paper_links: str = ""
    document_paths: str = ""


class GenerateGuideResponse(BaseModel):
    """Response model for guide generation"""
    generation_id: str
    status: str
    message: str


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "AI Guide Generator API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/api/v1/generate",
            "status": "/api/v1/status/{generation_id}",
            "download": "/api/v1/download/{generation_id}",
            "history": "/api/v1/history"
        }
    }


@app.post("/api/v1/generate", response_model=GenerateGuideResponse)
async def generate_guide(request: GenerateGuideRequest, background_tasks: BackgroundTasks):
    """Generate a guide asynchronously"""
    generation_id = str(uuid.uuid4())[:8]
    
    logger.info(f"New generation request: {generation_id}")
    
    # Add to background tasks
    background_tasks.add_task(
        run_guide_generation,
        generation_id,
        request.dict()
    )
    
    # Initialize status
    task_status[generation_id] = {
        "status": "processing",
        "progress": 0,
        "message": "Guide generation started"
    }
    
    return GenerateGuideResponse(
        generation_id=generation_id,
        status="processing",
        message="Guide generation started"
    )


@app.get("/api/v1/status/{generation_id}")
async def get_status(generation_id: str):
    """Check generation status"""
    # Check in-memory first
    if generation_id in task_status:
        return JSONResponse(content=task_status[generation_id])
    
    # Check database
    generation = db.get_generation(generation_id)
    if not generation:
        raise HTTPException(status_code=404, detail="Generation ID not found")
    
    return JSONResponse(content={
        "status": generation.status,
        "word_count": generation.word_count,
        "created_at": generation.created_at.isoformat() if generation.created_at else None
    })


@app.get("/api/v1/download/{generation_id}")
async def download_guide(generation_id: str):
    """Download generated guide"""
    # Check multiple possible paths
    possible_paths = [
        Path("outputs/getting_started_guide.md"),
        Path("./outputs/getting_started_guide.md"),
        Path("../outputs/getting_started_guide.md"),
    ]
    
    file_path = None
    for path in possible_paths:
        if path.exists():
            file_path = path
            break
    
    # If not found, try to find any .md file in outputs
    if not file_path:
        outputs_dir = Path("outputs")
        if outputs_dir.exists():
            md_files = list(outputs_dir.glob("*.md"))
            if md_files:
                file_path = md_files[0]
    
    if not file_path or not file_path.exists():
        raise HTTPException(status_code=404, detail="Guide not found. Check outputs folder.")
    
    return FileResponse(
        path=str(file_path),
        filename=f"guide_{generation_id}.md",
        media_type="text/markdown"
    )


@app.get("/api/v1/history")
async def get_history(limit: int = 10):
    """Get generation history"""
    try:
        history = db.get_recent_generations(limit=limit)
        
        return [
            {
                "id": h.generation_id,
                "created_at": h.created_at.isoformat() if h.created_at else None,
                "status": h.status,
                "word_count": h.word_count or 0,
                "execution_time": h.execution_time or 0,
                "sources_count": h.sources_count or 0
            }
            for h in history
        ]
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch history")


def run_guide_generation(generation_id: str, inputs: dict):
    """Background task to run guide generation"""
    try:
        logger.info(f"Starting generation: {generation_id}")
        
        # Update status
        task_status[generation_id]["status"] = "processing"
        task_status[generation_id]["progress"] = 10
        
        # Run flow
        flow = GuideGeneratorFlow()
        inputs['generation_id'] = generation_id
        result = flow.kickoff(inputs=inputs)
        
        # Update status
        task_status[generation_id]["status"] = "completed"
        task_status[generation_id]["progress"] = 100
        task_status[generation_id]["message"] = "Guide generated successfully"
        
        logger.info(f"Generation completed: {generation_id}")
        
    except Exception as e:
        task_status[generation_id]["status"] = "failed"
        task_status[generation_id]["error"] = str(e)
        logger.error(f"Generation failed: {generation_id} - {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)