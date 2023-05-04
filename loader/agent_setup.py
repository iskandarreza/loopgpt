from loopgpt.tools import BaseTool
from loader.tool_setup import (
    agent_tools, 
    file_read_tools, 
    file_write_tools,
    add_tools
) 

import loopgpt
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

class ConfigAgent:
    def __init__(self, agent_name: str, main_task: str):
        self.name: str = agent_name
        self.main_task: str = main_task
        self.agent = loopgpt.Agent()
        self.agent.name = self.name

        tools = self.agent.tools
        tools_list = agent_tools
        tool_set = add_tools(tool_set=tools, tools_list=tools_list)
        
        list_tools = ListTools(self.agent)
        tool_set[list_tools.id] = list_tools
        self.agent.tools = tool_set

        self.agent.description = f"An AI agent that will work with other AI agents to achieve consensus and complete the main task of {self.main_task}"
        self.agent.goals = [
            f"Our main task is {self.main_task}. ",
            f"""We will be successful in achiving our main task discussing by discussing our plans, reasons and thoughts with another agent or many agents and getting consensus. 
            They can help keep us on task, provide feedback, and steer us in the right direction so that our output produces quality and accurate results. 
            They can also run commands that we don't have access to. It might be a good idea to use the 'list_agents' command to see if there are any agents online. 
            We need to use the 'list_tools' command to see what commands are available to us. We need to find a way to relay commands to each other through 'message_agent' 
            so that we can run commands unavailable to the individual through the collective. """
        ]

        self.agent.constraints = [
            "We cannot run a command that is not available to us, but we can ask another agent in the collective if they cam run the command for us. "
            "If a command for example'command_name' returns the output 'Command command_name does not exist.', we should mark that tool as unavailable to us and check if other agents are able to run the command. "
            "We cannot proceed with any action or command without discussing our plans, reasons and thoughts with another agent or many agents and getting consensus. "
            "We are only allowed to use the following action commands without group concensus, but it is preferable to use them only when necessary :'message_agent', 'list_agents', 'list_tools'. ",
            "We may not use any other commands without seeking consensus from other agent or agents. This is to avoid us from repeating tasks that produce no results. "
        ]
    
    def sub_agent(self, sub_agent_name: str):
        _sub_agent = loopgpt.Agent()
        _sub_agent.name = sub_agent_name

        tools_list = agent_tools + file_read_tools + file_write_tools        
        tools = _sub_agent.tools
        tool_set = add_tools(tool_set=tools, tools_list=tools_list)
        
        list_tools = ListTools(_sub_agent)
        tool_set[list_tools.id] = list_tools
        _sub_agent.tools = tool_set

        _sub_agent.description = f"{_sub_agent.name}, an AI agent created specificially to help {self.name} complete their main task which is {self.main_task}."
        _sub_agent.goals = []
        _sub_agent.goals.append(f"""
            {self.name} has limited command access, the specifics unknown. We will help {self.name} achieve their main task of {self.main_task} by 
            ensuring they get the right command to use through us, {self.name} must share their plans, reasons and thoughts behind the action or command. 
            And when consensus has been reached after discussion, we will proceed to help them.""")
        _sub_agent.goals.append(f"We will run the 'list_tools' so we can share the results with {self.name}. ")

        _sub_agent.constraints = [
            f"We nee to find a way to relay to {self.name} the results of our decisions and actions through the message_agent command effectively that avoids confusion with system messages. "
            # f"Do not execute any file write commands from {self.name} outside of '{self.name}/' subdir and do not approve overwriting existing files. ",
            # f"Any files or resources saved to disk must only be in the '{self.name}/' subdir and not overwrite existing files. " ,
            # f"We must not agree to any 'write_to_file' or 'append_to_file' command outside of the {self.name} subdirectory. ",
            # f"We may only use the 'write_to_file' command for creating new files, it is not allowed for overwriting existing files.",
            # f"We may only use the 'make_directory' command within the {self.name} subdir. "
        ]

        self.agent.sub_agents[sub_agent_name] = [
            _sub_agent,
            _sub_agent.description
        ]

        return _sub_agent
    

    
    # def tool_proxy(self, tool_proxy_name: str):
    #     tool_proxy = loopgpt.Agent()
    #     tool_proxy.name = tool_proxy_name

    #     tools_list = agent_tools + file_read_tools + file_write_tools        
    #     tools = tool_proxy.tools
    #     tool_set = add_tools(tool_set=tools, tools_list=tools_list)
        
    #     tool_proxy.tools = tool_set

    #     tool_proxy.description = f"{tool_proxy.name}, an AI agent that advices {self.name} on what tools to use to achieve the main task of {self.main_task}."
    #     tool_proxy.goals = [
    #         f"The goal is to be a proxy for {self.name} and run commands that {self.name} is not able to run themselves because they do not have the tools. "
    #         f"Do not execute any file write commands from {self.name} outside of '{self.name}/' subdir and do not approve overwriting existing files. ",
    #         f"Any files or resources saved to disk must only be in the '{self.name}/' subdir and not overwrite existing files. You may only use the 'write_to_file' command for creating new files, it is not allowed for overwriting existing files." 
    #     ]

    #     tool_proxy.constraints = [
    #         f"You must not agree to any 'write_to_file' or 'append_to_file' command outside of the {self.name} subdirectory. You may only use the 'make_directory' command within the {self.name} subdir."
    #     ]

    #     # self.agent.constraints.insert(0, f"You do not have access to the 'write_to_file' or 'append_to_file' commands, you must ask {tool_proxy.name} if you can delegate the commands to them, which they may not if they need more information from you. Ask them how to proceed.")

    #     self.agent.sub_agents[tool_proxy_name] = [
    #         tool_proxy,
    #         tool_proxy.description
    #     ]

        # return tool_proxy

    # def recordkeeper(self, recordkeeper_name: str):
    #     recordkeeper = loopgpt.Agent()
    #     recordkeeper.name = recordkeeper_name

    #     tools_list = file_tools        
    #     tools = recordkeeper.tools
    #     tool_set = self.add_tools(tool_set=tools, tools_list=tools_list)
    #     recordkeeper.tools = tool_set

    #     recordkeeper.description = f"{recordkeeper.name}, an AI recordkeeping AI agent that stores data accurately, following proper formatting and convention for {self.name} based on it's relevance to the main task"
    #     recordkeeper.goals = [
    #         f"Do not approve any file write actions from {self.name} outside of '{self.name}/' subdir and do not approve overwriting existing files.",
    #         f"Any files or resources saved to disk must only be in the subdir '{self.name}/' and not overwrite existing files. You may only use the 'write_to_file' command for creating new files, it is not allowed for overwriting existing files." 
    #     ]

    #     recordkeeper.constraints = [
    #         f"You must not agree to any 'write_to_file' or 'append_to_file' command outside of the {self.name} subdirectory. You may only use the 'make_directory' command within the {self.name} subdir."
    #     ]

    #     self.agent.constraints.insert(0, f"You do not have access to the 'write_to_file' or 'append_to_file' commands, you must ask {recordkeeper.name} if you can delegate the commands to them, which they may not if they need more information from you. Ask them how to proceed.")

    #     self.agent.sub_agents[recordkeeper_name] = [
    #         recordkeeper,
    #         f"I am {recordkeeper_name}, recordkeeping agent that will store data on behalf of {self.name} by using the tools to record data to disk properly."
    #     ]

    #     return recordkeeper

    # def approver(self, approver_name: str):
    #     approver = loopgpt.Agent()
    #     approver.name = approver_name

    #     tools = approver.tools
    #     tools_list = [
    #         "message_agent",
    #         'list_agents',
    #         'list_files',
    #         'read_from_file'
    #     ] 
    #     tool_set = self.add_tools(tool_set=tools, tools_list=tools_list)
    #     approver.tools = tool_set

    #     message_agent = approver.tools.get("message_agent")
    #     approver.tools = {}
    #     approver.tools["message_agent"] = message_agent

    #     approver.description = f"{approver.name}, an AI agent that receives requests from {self.name} to approve actions to be taken about the main task, and approves or deny the requests based on it's relevance to the main task"
    #     approver.goals = [
    #         f"Do not approve the request from {self.name} if it does not relate to the main task of {self.main_task}",
    #         f"If an action is approved, instruct {self.name} to log to the task to '{self.name}/approved-tasks-{approver.name}.md' by appending an entry to the file after carrying out the action",
            
    #     ]

    #     approver.constraints = [
    #         f"Do not ask {self.name} for any work to do, you are to approve or deny tasks that {self.name} requests.",
    #     ]

    #     self.agent.goals.append(
    #         f"The way to achieve this goal is to ensure my requests as it relates to the main task go through the proper channels for approval. I need to message agent {approver.name} and provide information to them about what my main task is, and provide them with details on what my plan of action is to achieve the task so that they have context to approve or deny my actions. Then for all my next actions, I need to make sure agent {approver.name} gives me the go ahead to keep me focused on my task. ")
    #     self.agent.goals.append(
    #         f"Check if the file '{self.name}/approved-tasks-{approver.name}.md' exists and append the task that was approved there. If the file does not already exist, use the write to file command instead.")
    #     self.agent.constraints.insert(
    #         0, f"You require approval from agent {approver.name} for every action taken or command to be run, each time, with the exception of these commands: 'list_agents', 'message_agent'. Describe what your next plan is to agent {approver.name} with the request for approval. Do not proceed without approval, or new instructions from {approver.name}.")
    #     self.agent.constraints.insert(
    #         1, f"You are explicitly not allowed to use the following commands unless the user suggested it and agent {approver.name} approved its use: 'browser, google_search', 'shell'")

    #     # I found that a random uuid confuses the agent, it doesn't remember that 'id' and 'name' is not the same thing. Doesn't help that 'list_agents' shows items as ['uuid', 'purpose']
    #     self.agent.sub_agents[approver_name] = [
    #         approver,
    #         f"I am {approver_name}, coordinator agent that will orchestrate the tasks assigned to {self.name} by approving or denying their plans and actions to ensure they stay on task and their actions produce valid results. The  main task is {self.main_task}"
    #     ]

    #     return approver

    # def researcher(self, researcher_name):
    #     researcher = loopgpt.Agent()
    #     researcher.name = researcher_name
        
    #     tools = researcher.tools
    #     tools_list = [
    #         "message_agent",
    #         'list_agents',
    #         'google_search',
    #         'browser',
    #         'list_files',
    #         'read_from_file'
    #     ] 
    #     tool_set = self.add_tools(tool_set=tools, tools_list=tools_list)
    #     researcher.tools = tool_set

    #     researcher.description = f"{researcher_name}. a AI agent that conducts research for {self.name} to help achieve the main task by providing quality research"
    #     researcher.goals = [
    #         f"Do not carry out the research request from {self.name} if it does not relate to the main task of {self.main_task}",
    #         f"If a reasearch action is approved, instruct {self.name} to log to the research to '{self.name}/research-tasks-{researcher.name}.md' by appending an entry to the file"
    #     ]

    #     researcher.constraints = [
    #         f"You must not agree to any research if {self.name} is not able to explain how it is relevant to the main task of {self.main_task}"
    #     ]
    #     self.agent.goals.append(
    #         f"Check if the file '{self.name}/research-tasks-{researcher.name}.md' exists and append the research there with a clear heading. If the file does not already exist, use the write to file command instead.")
    #     self.agent.constraints.append(
    #         f"You are not allowed to conduct independent research, you must ask agent {researcher_name} to conduct research actions on your behalf. You need to explain to them what research you need done and how it relates to the main task in order for them to agree to conduct research for you.")

    #     self.agent.sub_agents[researcher_name] = [
    #         researcher, f"I am {researcher_name}, research agent that will conduct research for {self.name} by approving or denying their research plans and actions to ensure they stay on task and the research aligns with the main task and produces quality results. The main task is {self.main_task}"]
        
    #     return researcher
