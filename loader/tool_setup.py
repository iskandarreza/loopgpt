agent_tools = [
    "message_agent",
    'list_agents',
    'create_agent'
]

file_read_tools = [
    "list_files",
    "check_if_file_exists",
    "read_from_file"
]

file_write_tools = [
    "append_to_file",
    "write_to_file",
    "make_directory",
]

def add_tools(tool_set={}, tools_list=[]):
    tools = {}
    for tool in tools_list:
        _tool = tool_set.get(tool)
        tools[tool] = _tool
    return tools