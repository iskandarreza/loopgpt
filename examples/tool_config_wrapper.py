from loopgpt import AgentWrapper

class ToolConfig:
    # Tool set grouped by utility
    agent_tools = [
        "list_agents",
        "message_agent",
        "create_agent",
        "delete_agent",
    ]

    file_read_tools = [
        "list_files",
        "check_if_file_exists",
        "read_from_file",
        "get_cwd"
    ]

    file_write_tools = [
        "append_to_file",
        "write_to_file",
        "make_directory",
    ]

    code_tools = [
        "review_code",
        "improve_code",
        "write_tests"
    ]

    web_tools = [
        "google_search",
        "browser",
    ]

    dangerous_tools = [
        "execute_python_file",
        "shell"
    ]

    # misc uncategorized tools
    evaluate_math = ["evaluate_math"]
    ask_user = ["ask_user"]


    def add_tools(self, tool_set={}, tool_kit=[]):
        tools = {}
        for tool in tool_kit:
            _tool = tool_set.get(tool)
            tools[tool] = _tool
        return tools

tool_config = ToolConfig()
tool_kit = tool_config.web_tools + tool_config.agent_tools + tool_config.ask_user

wrapper = AgentWrapper()

tool_config_agent = wrapper.create_agent("Tool Testing Agent")
tool_set = tool_config_agent.tools 
tool_config_agent.tools = tool_config.add_tools(tool_set=tool_set, tool_kit=tool_kit)

print(tool_config_agent.tools)

# exec(open('examples/tool_config_wrapper.py').read()) 
# tool_config_agent.tools_prompt()