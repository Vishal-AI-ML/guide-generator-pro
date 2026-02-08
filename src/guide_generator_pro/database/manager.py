from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
from datetime import datetime
import os

from .models import Base, GuideGeneration
from ..utils.logger import setup_logger

logger = setup_logger("database")

class DatabaseManager:
    """Manage database operations"""
    
    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url or os.getenv("DATABASE_URL", "sqlite:///./guide_generator.db")
        self.engine = create_engine(self.db_url, echo=False)
        
        # Create tables
        Base.metadata.create_all(self.engine)
        
        # Create session factory
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        
        logger.info(f"Database initialized: {self.db_url}")
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def create_generation(
        self,
        generation_id: str,
        youtube_links: str = "",
        webpage_links: str = "",
        research_paper_links: str = "",
        document_paths: str = ""
    ) -> GuideGeneration:
        """Create new generation record"""
        session = self.get_session()
        
        try:
            # Count sources
            sources_count = sum(1 for s in [youtube_links, webpage_links, research_paper_links, document_paths] if s)
            
            generation = GuideGeneration(
                generation_id=generation_id,
                youtube_links=youtube_links,
                webpage_links=webpage_links,
                research_paper_links=research_paper_links,
                document_paths=document_paths,
                sources_count=sources_count,
                status='pending'
            )
            
            session.add(generation)
            session.commit()
            session.refresh(generation)
            
            logger.info(f"Created generation: {generation_id}")
            
            return generation
        
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create generation: {e}")
            raise
        
        finally:
            session.close()
    
    def update_generation(
        self,
        generation_id: str,
        **kwargs
    ) -> Optional[GuideGeneration]:
        """Update generation record"""
        session = self.get_session()
        
        try:
            generation = session.query(GuideGeneration).filter_by(generation_id=generation_id).first()
            
            if not generation:
                logger.warning(f"Generation not found: {generation_id}")
                return None
            
            for key, value in kwargs.items():
                if hasattr(generation, key):
                    setattr(generation, key, value)
            
            session.commit()
            session.refresh(generation)
            
            logger.info(f"Updated generation: {generation_id}")
            
            return generation
        
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to update generation: {e}")
            raise
        
        finally:
            session.close()
    
    def get_generation(self, generation_id: str) -> Optional[GuideGeneration]:
        """Get generation by ID"""
        session = self.get_session()
        
        try:
            generation = session.query(GuideGeneration).filter_by(generation_id=generation_id).first()
            return generation
        
        finally:
            session.close()
    
    def get_all_generations(self, limit: int = 50) -> List[GuideGeneration]:
        """Get all generations (most recent first)"""
        session = self.get_session()
        
        try:
            generations = session.query(GuideGeneration)\
                .order_by(desc(GuideGeneration.created_at))\
                .limit(limit)\
                .all()
            
            return generations
        
        finally:
            session.close()
    
    def get_recent_generations(self, limit: int = 10) -> List[GuideGeneration]:
        """Get recent generations"""
        return self.get_all_generations(limit=limit)