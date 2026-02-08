from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class GuideGeneration(Base):
    """Database model for guide generations"""
    
    __tablename__ = 'guide_generations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    generation_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Input sources
    youtube_links = Column(Text)
    webpage_links = Column(Text)
    research_paper_links = Column(Text)
    document_paths = Column(Text)
    
    # Outputs
    research_report = Column(Text)
    final_guide = Column(Text)
    
    # Metrics
    execution_time = Column(Float)
    research_time = Column(Float)
    writing_time = Column(Float)
    word_count = Column(Integer)
    sources_count = Column(Integer)
    
    # Status
    status = Column(String(20), default='pending')  # pending, processing, completed, failed
    success = Column(Boolean, default=False)
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    def __repr__(self):
        return f"<GuideGeneration(id={self.generation_id}, status={self.status})>"