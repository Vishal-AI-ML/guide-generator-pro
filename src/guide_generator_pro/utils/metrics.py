from dataclasses import dataclass, asdict
from typing import List, Dict
import json
from pathlib import Path
from datetime import datetime

@dataclass
class PerformanceMetrics:
    """Performance metrics for guide generation"""
    
    generation_id: str
    total_execution_time: float
    research_time: float
    writing_time: float
    total_sources_processed: int
    word_count: int
    success: bool
    errors: List[str]
    created_at: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    def save(self, output_dir: str = "outputs"):
        """Save metrics to JSON file"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        metrics_file = output_path / f"metrics_{self.generation_id}.json"
        
        with open(metrics_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return str(metrics_file)
    
    @staticmethod
    def load(filepath: str) -> 'PerformanceMetrics':
        """Load metrics from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return PerformanceMetrics(**data)


class MetricsTracker:
    """Track metrics during execution"""
    
    def __init__(self, generation_id: str):
        self.generation_id = generation_id
        self.start_time = None
        self.research_start = None
        self.research_end = None
        self.writing_start = None
        self.writing_end = None
        self.sources_count = 0
        self.errors = []
        self.word_count = 0
    
    def start(self):
        """Start tracking"""
        import time
        self.start_time = time.time()
    
    def start_research(self):
        """Start research phase"""
        import time
        self.research_start = time.time()
    
    def end_research(self):
        """End research phase"""
        import time
        self.research_end = time.time()
    
    def start_writing(self):
        """Start writing phase"""
        import time
        self.writing_start = time.time()
    
    def end_writing(self):
        """End writing phase"""
        import time
        self.writing_end = time.time()
    
    def add_error(self, error: str):
        """Add error to tracking"""
        self.errors.append(error)
    
    def finalize(self, final_guide: str) -> PerformanceMetrics:
        """Create final metrics report"""
        import time
        
        end_time = time.time()
        
        return PerformanceMetrics(
            generation_id=self.generation_id,
            total_execution_time=round(end_time - self.start_time, 2),
            research_time=round(self.research_end - self.research_start, 2) if self.research_end else 0,
            writing_time=round(self.writing_end - self.writing_start, 2) if self.writing_end else 0,
            total_sources_processed=self.sources_count,
            word_count=len(final_guide.split()) if final_guide else 0,
            success=len(self.errors) == 0,
            errors=self.errors,
            created_at=datetime.now().isoformat()
        )