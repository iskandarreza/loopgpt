from loopgpt.tools import BaseTool
import json

class ListTools(BaseTool):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    @property
    def desc(self):
        return "Use this command to list available tools."

    @property
    def args(self):
        return {}

    @property
    def resp(self):
        return {"supported_commands": "A Python List of command key and description values"}

    def run(self):
        tools = []
        for k, v in self.agent.tools.items():
            # v.agent = self.agent # is this even necessary?
            tools.append({k, v.prompt()})
        return {"supported_commands": f"{json.loads(tools)}"}
