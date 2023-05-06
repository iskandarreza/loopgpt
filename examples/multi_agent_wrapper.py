from loopgpt import BaseWrapper
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

class MultiAgentWrapper(BaseWrapper):
    def __init__(self, main_task) -> None:
          super().__init__(main_task)
          main_agent_id = self.create_agent("Main Agent")
          main_agent = super().get_agent(main_agent_id)
          main_agent.description = f"An AI agent that will work with other AI agents to achieve consensus and complete the main task of {main_task}"

          supporting_agent_id = self.create_agent("Supporting Agent")
          supporting_agent = super().get_agent(supporting_agent_id)
          supporting_agent.description = f"{supporting_agent.name}, an AI agent created specificially to help {main_agent.name} complete their main task which is {main_task}."

          main_agent.tools["list_agents"] = _ListAgents(self)
          supporting_agent.tools["list_agents"] = _ListAgents(self)
          main_agent.tools["message_agent"] = _MessageAgent(self)
          supporting_agent.tools["message_agent"] = _MessageAgent(self)


main_task = "listing available agents and the commands they can use to file "
wrapper = MultiAgentWrapper(main_task)
agents = wrapper.agents
main_id = list(agents.keys())[0]
support_id = list(agents.keys())[1]
print({main_id, support_id})
print(agents)

main_agent = wrapper.get_agent(main_id)
support_agent = wrapper.get_agent(support_id)

print(main_agent.tools)
print(support_agent.tools)
