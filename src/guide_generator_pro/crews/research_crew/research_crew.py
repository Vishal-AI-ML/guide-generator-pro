from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    YoutubeVideoSearchTool,
    YoutubeChannelSearchTool,
    ScrapeWebsiteTool,
    SeleniumScrapingTool,
    ArxivPaperTool,
    FileReadTool,
    PDFSearchTool,
    TXTSearchTool,
    MDXSearchTool,
    CodeDocsSearchTool,
    DirectoryReadTool
)

# Define tools
yt_video_search_tool = YoutubeVideoSearchTool()
yt_channel_search_tool = YoutubeChannelSearchTool()
web_scraping_tool = ScrapeWebsiteTool()
selenium_scraping_tool = SeleniumScrapingTool()
code_docs_search_tool = CodeDocsSearchTool()
arxiv_tool = ArxivPaperTool(download_pdfs=True, use_title_as_filename=True)
file_reader_tool = FileReadTool()
pdf_search_tool = PDFSearchTool()
text_search_tool = TXTSearchTool()
md_search_tool = MDXSearchTool()
directory_read_tool = DirectoryReadTool()


@CrewBase
class ResearchCrew():
    """ResearchCrew for multi-source research"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def research_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["research_manager"]
        )
        
    @agent
    def youtube_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["youtube_specialist"],
            tools=[yt_video_search_tool, yt_channel_search_tool]
        )
        
    @agent
    def web_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["web_specialist"],
            tools=[web_scraping_tool, selenium_scraping_tool, code_docs_search_tool]
        )
        
    @agent
    def arxiv_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["arxiv_specialist"],
            tools=[arxiv_tool]
        )
        
    @agent
    def document_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["document_specialist"],
            tools=[file_reader_tool, pdf_search_tool, text_search_tool, md_search_tool, directory_read_tool]
        )

    @task
    def research_compilation(self) -> Task:
        return Task(
            config=self.tasks_config["research_compilation"]
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.youtube_specialist(), self.arxiv_specialist(), self.web_specialist(), self.document_specialist()],
            tasks=[self.research_compilation()],
            verbose=True,
            process=Process.hierarchical,
            planning=False,
            manager_agent=self.research_manager()
        )