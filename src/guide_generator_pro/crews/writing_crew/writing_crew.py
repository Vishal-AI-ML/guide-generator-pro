from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class WritingCrew():
    """WritingCrew for guide creation"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def technical_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["technical_writer"]
        )
    
    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config["content_editor"]
        )

    @task
    def write_getting_started_guide(self) -> Task:
        return Task(
            config=self.tasks_config["write_getting_started_guide"],
            agent=self.technical_writer()  # ADD THIS
        )
        
    @task
    def review_and_polish_guide(self) -> Task:
        return Task(
            config=self.tasks_config["review_and_polish_guide"],
            agent=self.content_editor()  # ADD THIS
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )