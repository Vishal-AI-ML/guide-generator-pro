from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from typing import Optional
from dotenv import load_dotenv
import time
import uuid

from .crews.research_crew.research_crew import ResearchCrew
from .crews.writing_crew.writing_crew import WritingCrew
from .database.manager import DatabaseManager
from .utils.logger import setup_logger
from .utils.metrics import MetricsTracker

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger("guide_generator_flow")


class ResearchFlowState(BaseModel):
    """State for the guide generation flow"""
    
    # Generation ID
    generation_id: str = ""
    
    # User inputs
    youtube_links: Optional[str] = ""
    document_paths: Optional[str] = ""
    webpage_links: Optional[str] = ""
    research_paper_links: Optional[str] = ""
    
    # Outputs
    research_report: str | None = None
    final_guide: str | None = None


class GuideGeneratorFlow(Flow[ResearchFlowState]):
    """
    Production-grade guide generation flow with:
    - Error handling & logging
    - Performance metrics
    - Database storage
    """
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.metrics = None
    
    @start()
    def receive_user_inputs(self) -> str:
        """Receive and validate user inputs"""
        logger.info("=" * 70)
        logger.info("GUIDE GENERATOR FLOW STARTED")
        logger.info("=" * 70)
        
        # Generate unique ID
        self.state.generation_id = str(uuid.uuid4())[:8]
        
        # Initialize metrics tracker
        self.metrics = MetricsTracker(self.state.generation_id)
        self.metrics.start()
        
        # Log sources
        sources_provided = []
        if self.state.youtube_links:
            sources_provided.append("YouTube")
        if self.state.webpage_links:
            sources_provided.append("Web Pages")
        if self.state.document_paths:
            sources_provided.append("Documents")
        if self.state.research_paper_links:
            sources_provided.append("Research Papers")
        
        if not sources_provided:
            logger.warning("⚠️  WARNING: No sources provided!")
            return "no_sources"
        
        self.metrics.sources_count = len(sources_provided)
        logger.info(f"Sources provided: {', '.join(sources_provided)}")
        
        # Create database record
        try:
            self.db.create_generation(
                generation_id=self.state.generation_id,
                youtube_links=self.state.youtube_links or "",
                webpage_links=self.state.webpage_links or "",
                research_paper_links=self.state.research_paper_links or "",
                document_paths=self.state.document_paths or ""
            )
            logger.info(f"Database record created: {self.state.generation_id}")
        except Exception as e:
            logger.error(f"Database error: {e}")
        
        logger.info("=" * 70)
        return "inputs_received"
    
    @listen(receive_user_inputs)
    def run_research_crew(self, prev_output) -> str:
        """Execute Research Crew"""
        if prev_output == "no_sources":
            logger.error("Skipping research crew - no sources provided")
            return "research_skipped"
        
        logger.info("=" * 70)
        logger.info("CREW 1: RESEARCH CREW (Hierarchical)")
        logger.info("=" * 70)
        
        try:
            # Update database status
            self.db.update_generation(
                self.state.generation_id,
                status='processing'
            )
            
            # Start metrics
            self.metrics.start_research()
            
            # Initialize and run research crew
            research_crew = ResearchCrew().crew()
            logger.info("Delegating research tasks to specialists...")
            
            result = research_crew.kickoff(inputs={
                "youtube_links": self.state.youtube_links or "Not provided",
                "webpage_links": self.state.webpage_links or "Not provided",
                "research_paper_links": self.state.research_paper_links or "Not provided",
                "document_paths": self.state.document_paths or "Not provided"
            })
            
            # Store result
            self.state.research_report = result.raw
            
            # End metrics
            self.metrics.end_research()
            
            # Update database
            self.db.update_generation(
                self.state.generation_id,
                research_report=result.raw,
                research_time=self.metrics.research_end - self.metrics.research_start
            )
            
            logger.info("=" * 70)
            logger.info("RESEARCH CREW COMPLETED")
            logger.info("=" * 70)
            
            return "research_complete"
            
        except Exception as e:
            logger.error(f"ERROR in Research Crew: {str(e)}", exc_info=True)
            self.metrics.add_error(str(e))
            
            # Update database
            self.db.update_generation(
                self.state.generation_id,
                status='failed',
                error_message=str(e)
            )
            
            return "research_failed"
    
    @listen(run_research_crew)
    def run_writing_crew(self, prev_output) -> str:
        """Execute Writing Crew"""
        if prev_output in ["research_skipped", "research_failed"]:
            logger.error("Skipping writing crew - research failed")
            return "writing_skipped"
        
        logger.info("=" * 70)
        logger.info("✍️  CREW 2: WRITING CREW (Sequential)")
        logger.info("=" * 70)
        
        try:
            # Start metrics
            self.metrics.start_writing()
            
            # Initialize and run writing crew
            writing_crew = WritingCrew().crew()
            logger.info("Transforming research into beginner-friendly guide...")
            
            result = writing_crew.kickoff(inputs={
                "research_report": self.state.research_report
            })
            
            # Store result
            self.state.final_guide = result.raw
            
            # End metrics
            self.metrics.end_writing()
            
            # Generate final metrics
            final_metrics = self.metrics.finalize(self.state.final_guide)
            
            # Save metrics to file
            metrics_file = final_metrics.save()
            logger.info(f"Metrics saved: {metrics_file}")
            
            # Update database
            self.db.update_generation(
                self.state.generation_id,
                final_guide=result.raw,
                writing_time=self.metrics.writing_end - self.metrics.writing_start,
                execution_time=final_metrics.total_execution_time,
                word_count=final_metrics.word_count,
                status='completed',
                success=True
            )
            
            logger.info("=" * 70)
            logger.info("WRITING CREW COMPLETED")
            logger.info("=" * 70)
            logger.info(f"📝 Guide: {final_metrics.word_count} words")
            logger.info(f"⏱️  Total time: {final_metrics.total_execution_time}s")
            logger.info("=" * 70)
            
            return "guide_complete"
            
        except Exception as e:
            logger.error(f"ERROR in Writing Crew: {str(e)}", exc_info=True)
            self.metrics.add_error(str(e))
            
            # Update database
            self.db.update_generation(
                self.state.generation_id,
                status='failed',
                error_message=str(e)
            )
            
            return "writing_failed"