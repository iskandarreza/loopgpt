from loopgpt import AgentWrapper, AgentRegistry
from loopgpt.tools.agent_manager import MessageAgent, ListAgents

class _MessageAgent(MessageAgent):
    def __init__(self, wrapper):
        self._wrapper = wrapper

    def run(self, id, message):
        if id not in self._wrapper.agents:
            return {"resp": "AGENT NOT FOUND!"}
        resp = self._wrapper.agents[id][0].chat(message)
        return {"resp": resp}

class _ListAgents(ListAgents):
    def __init__(self, wrapper):
        self._wrapper = wrapper

    @property
    def resp(self):
        return {
            "agents": "List of available agents, array of objects {id, name, description}"
        }

    def run(self):
        return f'"agents": "{self._wrapper._agents_roster}"'

class MultiAgentTaskRegistry(AgentRegistry):
    def __init__(self, registry_name) -> None:
          super().__init__(registry_name)
          self._agents_roster = {}

    @property
    def agents_roster(self):
        return self._agents_roster
    
    def register_agent(self, agent, main_task):
        agent_id = super().register_agent(agent)
        self._agents_roster[agent_id] = [{"name": agent.name}, {"task": [{main_task}]}]
    
def setup_agent_registry(main_task: str):
    agentWrapper = AgentWrapper()
    registry = MultiAgentTaskRegistry("Multi Agent Registry")

    main_agent = agentWrapper.create_agent("Main Agent")
    main_agent.description = f"An AI agent that will work with other AI agents to achieve consensus and complete the main task of {main_task}"
    main_agent.tools["list_agents"] = _ListAgents(registry)
    main_agent.tools["message_agent"] = _MessageAgent(registry)
    registry.register_agent(main_agent, main_agent.description)

    supporting_agent = agentWrapper.create_agent("Supporting Agent")
    supporting_agent.description = f"{supporting_agent.name}, an AI agent created specificially to help {main_agent.name} complete their main task which is {main_task}."
    supporting_agent.tools["list_agents"] = _ListAgents(registry)
    supporting_agent.tools["message_agent"] = _MessageAgent(registry)
    registry.register_agent(supporting_agent, supporting_agent.description)

    return registry

main_task = "listing available agents and the commands they can use to file "
registry = setup_agent_registry(main_task)

print(f""" 

--- List of agents ---
{registry.agents}""")


print(f""" 

--- Agent duty roster ---
{registry._agents_roster}""")

# exec(open("examples/multi_agent_wrapper.py").read())
