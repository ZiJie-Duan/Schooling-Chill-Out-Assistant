
class AgentBrick:

    def __init__(self, 
                brick_name: str, # function name
                description: str, # function description
                front_prompt: str,
                back_prompt: str = None,
                brick_type: str = "mid", # head, mid, end
                ) -> None:
    
        self.brick_name = brick_name
        self.description = description
        self.front_prompt = front_prompt
        # provides the prompt to help upper level agent make decision
        self.back_prompt = back_prompt
        # provides the prompt for next action
        self.brick_type = brick_type
        self.actions = []
        self.parameters = {}
        self.call_back = None
    

    def set_call_back(self, parameters: dict, func: object):
        """set parameters for the brick
            {
                "name":{"type": "type","description": "description"},
                "xxxx":{"type": "xxxx","description": "xxxxx"},
                "xxxx":{"type": "xxxx", "enum": ["xxxxx", "xxxxx"]}
            }
        """
        self.parameters = parameters
        self.call_back = func
    

    def add_action(self, action: object):
        self.actions.append(action)


class AgentSystem:

    def __init__(self, root_brick) -> None:
        self.root_brick = root_brick
    
    def show_agent(self):
        print(self.root_brick.brick_name)

        root_brick = self.root_brick
        for brick in root_brick.actions:
            print(brick.brick_name)
            
    



