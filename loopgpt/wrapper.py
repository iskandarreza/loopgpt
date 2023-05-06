from loopgpt import Agent
from uuid import uuid4

# The `AgentWrapper` class contains methods to create and assign sub-agents to an assignee's list of
# sub-agents.
class AgentWrapper:
    def __init__(self) -> None:
        pass

    def create_agent(self, agent_name: str):
        """
        This function creates a new agent object with a unique ID and a given name.
        @param {str} agent_name - The parameter `agent_name` is a string that represents the name of the
        agent that we want to create.
        @returns A new instance of the `Agent` class with a randomly generated ID and the name provided
        as an argument.
        """
        new_agent = Agent()
        new_agent.id = uuid4().hex[:8]
        new_agent.name = agent_name

        return new_agent
    
    def assign_subagent(self, sub_agent, assignee):
        """
        This function assigns a sub-agent to an assignee's list of sub-agents.
        @param sub_agent - The sub_agent parameter is an object representing a sub-agent that is being
        assigned to an assignee.
        @param assignee - The assignee parameter is an object that has a dictionary attribute called
        "sub_agents". This method is adding a new sub_agent to the assignee's sub_agents dictionary.
        """
        assignee.sub_agents[f"{sub_agent.id}"] = [
            sub_agent,
            sub_agent.description
        ]

# The AgentRegistry class allows for registering and retrieving agents with unique IDs and
# descriptions.
class AgentRegistry:
    def __init__(self, registry_name: str)-> None:
        self._registry_name = registry_name
        self._agents = {}

    @property
    def agents(self):
        return self._agents
    
    def register_agent(self, agent):
        id = uuid4().hex[:8]
        self._agents[id] = [agent, agent.description]
        return id
    
    def get_agent(self, agent_id):
        return self.agents[agent_id][0]
