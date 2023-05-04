from loader.agent_setup import ConfigAgent
from loopgpt.constants import AgentStates

class GuardRails:
    def __init__(self) -> None:
        agent_name = "2222-Brave-Prevail"
        # main_task = f"finding what commands {agent_name} can run and what command other agents can run, then writing the results of our collective capabilities, and the results of our individual capabilites to file "
        main_task = f"finding out what commands {agent_name} can run by themselves and what command require another agent to intervene "

        config = ConfigAgent(agent_name=agent_name, main_task=main_task)
        agent = config.agent

        agent.goals.append('If the main task is complete, we can explore and test the capabilites of each of the available commands, then document the results.')

        sub_agent_name = "6666-Innovative-Invent"
        sub_agent = config.sub_agent(sub_agent_name=sub_agent_name)

        print(f'Sub Agent: {sub_agent_name}')
        print(sub_agent.goals_prompt())
        print(sub_agent.constraints_prompt())
        print(sub_agent.tools_prompt())
        
        print()
        print(f'Agent: {agent_name}')
        print(agent.goals_prompt())
        print(agent.constraints_prompt())
        print(agent.tools_prompt())
        
        agent.sub_agents[sub_agent_name][0].state = AgentStates.START
        agent.state = AgentStates.START

        agent.cli()

        
        # for k, v in agent.sub_agents.items():

        #     print(k)
        #     print(v[1])


GuardRails()