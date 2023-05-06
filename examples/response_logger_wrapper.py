from loopgpt import AgentWrapper

import json
import requests

def post_data(data: dict, url_params: str, url: str):
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost'
    }

    json_data = json.dumps({"data": data}, sort_keys=True, indent=4)
    requests.post(f"{url}{url_params}", headers=headers, json=json.loads(json_data))

class ResponseLoggerWrapper(AgentWrapper):
    def __init__(self) -> None:
        super().__init__()
        self._cycle_count = 0
        
    @property
    def cycle_count(self):
        return self._cycle_count
    
    # keep track of how many cycles it has run
    def increment_cycle_count(self):
        self._cycle_count += 1
    
    def get_system_messages(self, agent):
        for msg in agent.history[::-1]:
            if msg["role"] == "system":
                return msg["content"]
        return ""
    
    ## start the loop, log the responses
    def run_loop(self, agent, count = 1):
        print(f"""
                --- running loop for agent {agent.name} ---
            """)
        for i in range(count):
            log_data = {}

            print("""
                --- getting agent response ---
            """)
            response = agent.chat()             
            response_json = json.dumps(response, indent=4)
            
            print((
                f'--- agent {agent.name} full response at count {i} cycle {self.cycle_count} ---'
            ))
            print(response_json)

            # run tools and log response
            if "command" in response:
                command = response["command"]
                if (
                    isinstance(command, dict)
                    and "name" in command
                    and "args" in command
                ):
                    if command["name"]:
                        print(
                            "command",
                            f"{command['name']}, Args: {command['args']}",
                            end="\n\n",
                        )
                    cmd = agent.staging_tool.get("name", agent.staging_tool)
                    if cmd != "task_complete":
                        agent.run_staging_tool()


            ## Post the data to an endpoint for logging
            print((
                f'--- agent {agent.name} log data to send to server ---'
            ))
            log_data["cycle_count"] = self.cycle_count
            log_data["agent_name"] = agent.name
            log_data["agent_state"] = agent.state
            log_data["goals"] = agent.goals_prompt()
            log_data["plan"] = agent.plan_prompt()
            log_data['system_message'] = self.get_system_messages(agent)
            
            if agent.staging_tool != None:
                log_data["staging_tool"] = agent.staging_tool
            if agent.staging_response != None:
                log_data["staging_response"] = agent.staging_response
            if agent.tool_response != None:
                log_data["tool_response"] = agent.tool_response

            print(log_data)
            post_data(log_data, "logdata", "http://localhost:5050/api/")
            self.increment_cycle_count()

    def setup_agents(self, main_task):
        main_agent_name = "Main Agent"
        main_agent = self.create_agent(main_agent_name)
        main_agent.description = f"An AI agent that will work with other AI agents to achieve consensus and complete the main task of {main_task}"
        main_agent.goals.append(f"Our main task is {main_task}. ")
        
        secondary_agent_name = "Support Agent"
        secondary_agent = self.create_agent(secondary_agent_name)
        secondary_agent.description = f"{secondary_agent_name}, an AI agent created specificially to help {main_agent_name} complete their main task which is {main_task}."

        self.assign_subagent(secondary_agent, main_agent)

        return main_agent

main_task = "listing available agents and the commands they can use to file "
wrapper = ResponseLoggerWrapper()
main_agent = wrapper.setup_agents(main_task)

wrapper.run_loop(main_agent, 5)
# exec(open("examples/response_logger_wrapper.py").read())
