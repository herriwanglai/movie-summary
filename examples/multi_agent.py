"""Example: Multi-agent collaboration"""

from src.orchestrator.multi_agent import MultiAgentCoordinator, Agent, AgentRole, AgentTask

# Define custom agents
class VideoAnalysisAgent(Agent):
    """Agent specialized in video analysis"""

    def __init__(self):
        super().__init__("video_analyzer", AgentRole.VIDEO_PROCESSOR)

    def execute_task(self, task):
        if task.action == "analyze_cinematography":
            return {
                "camera_movements": ["tracking shots", "static frames"],
                "composition": "rule of thirds",
                "lighting": "high contrast"
            }
        return {"error": "Unknown action"}


class ScriptAnalysisAgent(Agent):
    """Agent specialized in script analysis"""

    def __init__(self):
        super().__init__("script_analyzer", AgentRole.SCRIPTWRITER)

    def execute_task(self, task):
        if task.action == "analyze_structure":
            return {
                "structure": "three-act",
                "pacing": "good",
                "dialogue_quality": 8.5
            }
        return {"error": "Unknown action"}


# Create coordinator
coordinator = MultiAgentCoordinator()

# Register agents
video_agent = VideoAnalysisAgent()
script_agent = ScriptAnalysisAgent()

coordinator.register_agent(video_agent)
coordinator.register_agent(script_agent)

# Define workflow
tasks = [
    AgentTask(
        task_id="video_analysis",
        agent_role=AgentRole.VIDEO_PROCESSOR,
        action="analyze_cinematography",
        parameters={}
    ),
    AgentTask(
        task_id="script_analysis",
        agent_role=AgentRole.SCRIPTWRITER,
        action="analyze_structure",
        parameters={},
        dependencies=["video_analysis"]  # Depends on video analysis
    )
]

# Execute workflow
results = coordinator.execute_workflow(tasks)

print("Video Analysis:", results["video_analysis"])
print("Script Analysis:", results["script_analysis"])

# Agent communication example
coordinator.send_message(
    sender="video_analyzer",
    receiver="script_analyzer",
    content={"visual_themes": ["isolation", "transformation"]},
    message_type="notification"
)

coordinator.process_all_messages()
