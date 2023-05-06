from loopgpt import Agent
from uuid import uuid4

class BaseWrapper:
    def __init__(self, main_task: str)-> None:
        self._agents = {}
        self._agents_roster = []
        self._message_queue = []
        self._main_task = f"{main_task} "

    @property
    def agents(self):
        return self._agents
    @property
    def agents_roster(self):
        return self._agents_roster
    @property
    def message_queue(self):
        return self._message_queue
    
    def register_agent(self, agent):
        id = uuid4().hex[:8]
        self._agents[id] = [agent, self._main_task]
        self.agents_roster.append({"id":f"{id}", "name":f"{agent.name}"})
        return id
    
    def create_agent(self, agent_name):
        new_agent = Agent()
        new_agent.name = agent_name
        new_agent.description = f"{new_agent.description} for the purpose of {self._main_task}"
        new_agent.goals.append(self._main_task)
        new_agent_id = self.register_agent(new_agent)

        return new_agent_id
    
    def assign_subagent(self, sub_agent, assignee, sub_agent_id=None):
        if sub_agent_id is None: sub_agent_id = uuid4().hex[:8] # probably not the best solution
        assignee.sub_agents[sub_agent_id] = [
            sub_agent,
            sub_agent.description
        ]

    def get_agent(self, agent_id):
        return self.agents[agent_id][0]
