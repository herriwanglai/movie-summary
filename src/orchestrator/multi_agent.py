"""Multi-agent coordination system"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class AgentRole(Enum):
    """Agent roles in the system"""
    VIDEO_PROCESSOR = "video_processor"
    AUDIO_PROCESSOR = "audio_processor"
    SUMMARIZER = "summarizer"
    SCENE_ANALYZER = "scene_analyzer"
    SCRIPTWRITER = "scriptwriter"
    STORYBOARD_CREATOR = "storyboard_creator"


@dataclass
class AgentMessage:
    """Message between agents"""
    sender: str
    receiver: str
    content: Any
    message_type: str  # 'request', 'response', 'notification'


@dataclass
class AgentTask:
    """Task for an agent"""
    task_id: str
    agent_role: AgentRole
    action: str
    parameters: Dict[str, Any]
    dependencies: List[str] = None  # Task IDs this depends on

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class Agent:
    """Base agent class"""

    def __init__(self, name: str, role: AgentRole):
        """
        Initialize agent

        Args:
            name: Agent name
            role: Agent role
        """
        self.name = name
        self.role = role
        self.message_queue: List[AgentMessage] = []

    def receive_message(self, message: AgentMessage):
        """Receive a message"""
        self.message_queue.append(message)

    def process_messages(self) -> List[AgentMessage]:
        """Process queued messages and return responses"""
        responses = []
        for message in self.message_queue:
            response = self.handle_message(message)
            if response:
                responses.append(response)
        self.message_queue.clear()
        return responses

    def handle_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Handle a single message (to be overridden)"""
        return None

    def execute_task(self, task: AgentTask) -> Any:
        """Execute a task (to be overridden)"""
        raise NotImplementedError


class MultiAgentCoordinator:
    """Coordinate multiple agents working together"""

    def __init__(self):
        """Initialize coordinator"""
        self.agents: Dict[str, Agent] = {}
        self.task_results: Dict[str, Any] = {}
        self.task_status: Dict[str, str] = {}  # 'pending', 'running', 'completed', 'failed'

    def register_agent(self, agent: Agent):
        """
        Register an agent

        Args:
            agent: Agent instance
        """
        self.agents[agent.name] = agent

    def send_message(self, sender: str, receiver: str, content: Any, message_type: str = 'request'):
        """
        Send message from one agent to another

        Args:
            sender: Sender agent name
            receiver: Receiver agent name
            content: Message content
            message_type: Type of message
        """
        if receiver not in self.agents:
            raise ValueError(f"Agent '{receiver}' not found")

        message = AgentMessage(
            sender=sender,
            receiver=receiver,
            content=content,
            message_type=message_type
        )

        self.agents[receiver].receive_message(message)

    def broadcast_message(self, sender: str, content: Any, message_type: str = 'notification'):
        """
        Broadcast message to all agents

        Args:
            sender: Sender agent name
            content: Message content
            message_type: Type of message
        """
        for agent_name in self.agents:
            if agent_name != sender:
                self.send_message(sender, agent_name, content, message_type)

    def execute_workflow(self, tasks: List[AgentTask]) -> Dict[str, Any]:
        """
        Execute a workflow of tasks with dependencies

        Args:
            tasks: List of AgentTask objects

        Returns:
            Dictionary of task results
        """
        # Initialize task status
        for task in tasks:
            self.task_status[task.task_id] = 'pending'

        # Execute tasks respecting dependencies
        while any(status == 'pending' for status in self.task_status.values()):
            for task in tasks:
                if self.task_status[task.task_id] == 'pending':
                    # Check if dependencies are met
                    dependencies_met = all(
                        self.task_status.get(dep) == 'completed'
                        for dep in task.dependencies
                    )

                    if dependencies_met:
                        self._execute_task(task)

        return self.task_results

    def _execute_task(self, task: AgentTask):
        """Execute a single task"""
        self.task_status[task.task_id] = 'running'

        # Find agent with matching role
        agent = None
        for a in self.agents.values():
            if a.role == task.agent_role:
                agent = a
                break

        if not agent:
            self.task_status[task.task_id] = 'failed'
            self.task_results[task.task_id] = {
                "error": f"No agent found for role {task.agent_role}"
            }
            return

        try:
            result = agent.execute_task(task)
            self.task_results[task.task_id] = result
            self.task_status[task.task_id] = 'completed'
        except Exception as e:
            self.task_status[task.task_id] = 'failed'
            self.task_results[task.task_id] = {
                "error": str(e)
            }

    def process_all_messages(self):
        """Process messages for all agents"""
        responses = []
        for agent in self.agents.values():
            agent_responses = agent.process_messages()
            responses.extend(agent_responses)

        # Deliver responses
        for response in responses:
            if response.receiver in self.agents:
                self.agents[response.receiver].receive_message(response)

    def get_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all agents"""
        return {
            name: {
                "role": agent.role.value,
                "queued_messages": len(agent.message_queue)
            }
            for name, agent in self.agents.items()
        }

    def collaborative_analysis(
        self,
        video_path: str,
        scene_analyzer_fn: Callable,
        scriptwriter_fn: Callable
    ) -> Dict[str, Any]:
        """
        Run collaborative analysis where agents work together

        Args:
            video_path: Path to video
            scene_analyzer_fn: Function for scene analysis
            scriptwriter_fn: Function for scriptwriting analysis

        Returns:
            Combined analysis results
        """
        results = {}

        # Scene analyzer produces initial analysis
        print("🎬 Scene Analyzer: Analyzing visual storytelling...")
        scene_analysis = scene_analyzer_fn(video_path)
        results['scene_analysis'] = scene_analysis

        # Scriptwriter reviews and provides feedback
        print("✍️  Scriptwriter: Providing expert analysis...")
        script_feedback = scriptwriter_fn(scene_analysis)
        results['script_feedback'] = script_feedback

        # Combine insights
        results['combined_insights'] = self._combine_insights(
            scene_analysis,
            script_feedback
        )

        return results

    def _combine_insights(
        self,
        scene_analysis: Any,
        script_feedback: Any
    ) -> Dict[str, Any]:
        """Combine insights from multiple agents"""
        return {
            "visual_storytelling": scene_analysis,
            "narrative_structure": script_feedback,
            "synthesis": "Combined analysis from visual and narrative perspectives"
        }
