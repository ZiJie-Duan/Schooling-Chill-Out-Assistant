from module.chrome_control import Unimelb_Lecture_Rec_CC
from module.config import Config
from agent.agent import AgentSystem, AgentBrick


def get_subtitle_info(info):
    """
    get subtitle information from chrome
    """
    print("Record_important_information_function：",info)
    return {}

def Ignore_irrelevant_information(info):
    """
    get subtitle information from chrome
    """
    print("Record_important_information_function：",info)
    return {}

important_brick = AgentBrick("Record_important_information", "Record important information, try to ensure the completeness of the information")
important_brick.front_prompt = "If you find important information (time, place, behavior-related), please extract and record important information"
important_brick.brick_think = "do"
important_brick.action_type = "enviroment"
important_brick.call_back = get_subtitle_info
important_brick.parameters = {"info":{"type": "string","description": "Important Information"}}

ignore_brick = AgentBrick("Ignore_irrelevant_information", "Ignore irrelevant information")
ignore_brick.front_prompt = "If you find that this sentence doesn't contain any important information, please choose to ignore"
ignore_brick.brick_think = "do"
ignore_brick.action_type = "enviroment"
ignore_brick.call_back = Ignore_irrelevant_information
ignore_brick.parameters = {"info":{"type": "string","description": "Please fill in <<<NONE>>> surrounded by dashes at the parameter info"}}

root_brick = AgentBrick("Decision_root_node", "The beginning of intelligent agent behavior")
root_brick.back_prompt = "The above information is a subtitle information, please choose the next action based on the subtitle information"
root_brick.brick_think = "think"
root_brick.action_type = "multi"
root_brick.actions = [important_brick, ignore_brick]

agent_system = AgentSystem(root_brick,api_key="")
print(agent_system.run(""))
print(agent_system.memo.data)
