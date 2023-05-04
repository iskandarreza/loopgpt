from loopgpt.tools.base_tool import BaseTool
from loader.tool_setup import (
    agent_tools, 
    file_read_tools, 
    file_write_tools,
    add_tools
) 
from typing import *
from uuid import uuid4

import json


class _AgentManagerTool(BaseTool):
    pass


class CreateAgent(_AgentManagerTool):
    @property
    def args(self):
        return {
            "name": "Agent name format: '4-digits-adjective-verb'",
            "task": "Specific task for agent",
            "prompt": "The prompt",
        }

    @property
    def resp(self):
        return {
            "id": "Unique ID of new agent.",
            "resp": "Response from new agent.",
        }

    def run(self, name="", task="", prompt=""):
        from loopgpt.agent import Agent

        agent = Agent(
            name=name, description=f"An agent for performing this specific task: {task}"
        )
        
        tools_list = agent_tools + file_read_tools + file_write_tools        
        tools = agent.tools
        tool_set = add_tools(tool_set=tools, tools_list=tools_list)
        
        agent.tools = tool_set

        id = uuid4().hex[:8]
        self.agent.sub_agents[id] = (Agent(), task)
        resp = agent.chat(prompt)
        return {"uuid": id, "resp": resp}


class MessageAgent(_AgentManagerTool):
    @property
    def args(self):
        return {
            "id": "Agent id.",
            "message": "The message",
        }

    @property
    def resp(self):
        return {"resp": "Response from the agent."}

    def run(self, id, message):
        if id not in self.agent.sub_agents:
            agent_list = [[k, v[1]] for k, v in self.agent.sub_agents.items()]
            return {"resp": f"AGENT NOT FOUND! Agent List: {json.dumps(agent_list)}"}
        resp = self.agent.sub_agents[id][0].chat(message)
        return {"resp": resp}


class DeleteAgent(_AgentManagerTool):
    @property
    def args(self):
        return {"id": "Agent id"}

    @property
    def resp(self):
        return {"success": "true or false"}

    def run(self, id):
        try:
            self.agent.sub_agents.pop(id)
            return {"resp": "Deleted."}
        except KeyError:
            return {f"resp": "Specified agent (id={id} not found.)"}


class ListAgents(_AgentManagerTool):
    @property
    def args(self):
        return {}

    @property
    def resp(self):
        return {
            "agents": "List of available agents, where each item is of the form [agent id, task]"
        }

    def run(self):
        return [[k, v[1]] for k, v in self.agent.sub_agents.items()]


AgentManagerTools = [CreateAgent, MessageAgent, DeleteAgent, ListAgents]
