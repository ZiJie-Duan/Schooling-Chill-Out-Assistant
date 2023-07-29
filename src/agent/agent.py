from agent.memo import Memo
from agent.gpt_api import GPT_API
from typing import Any, List, Dict
import time
import pprint
import json

class AgentBrick:
    """
    AgentBrick is the basic unit of agent system.
    It is a function that can be called by other bricks.
    Args:
        brick_name: the name of the brick
        description: the description of the brick
        front_prompt: the prompt to help upper level agent make decision
        back_prompt: the prompt for next action, the scenario
        brick_think: "think" or "do"
            "think": make the LLM to think
            "do": will not make the LLM to think, 
                  but it will call the call_back function
        action_type: "multi" or "single" or "enviroment"
            "multi": only think mode can be multi, make dicision by LLM
            "single": wither think or do mode, call the only next brick
            "enviroment": wither think or do mode, call the enviroment
        actions: the list of bricks that can be called by this brick
        parameters: the parameters for the brick
        call_back: the function that will be called when the brick is called
    
    set parameters for the brick
    {
        "name":{"type": "type","description": "description"},
        "xxxx":{"type": "xxxx","description": "xxxxx"},
        "xxxx":{"type": "xxxx", "enum": ["xxxxx", "xxxxx"]}
    }
    """

    def __init__(self, 
                brick_name: str, # function name
                description: str, # function description
                front_prompt: str = "",
                back_prompt: str = "",
                brick_think: str = "", # "think" or "do"
                action_type: str = "", # "multi" or "single" or "enviroment"
                actions: list = [],
                parameters: dict = {},
                call_back: object = None
                ) -> None:
    
        self.brick_name = brick_name
        self.description = description
        self.front_prompt = front_prompt
        # provides the prompt to help upper level agent make decision
        self.back_prompt = back_prompt
        # provides the prompt for next action
        self.brick_think = brick_think
        self.action_type = action_type
        self.actions = actions
        self.parameters = parameters
        self.call_back = call_back



class AgentSystem:

    def __init__(self, root_brick,
                 memopath = "memo.json",
                 api_key = "") -> None:
        
        self.gpt_api = GPT_API(api_key)
        self.memo = Memo(memopath)
        self.root_brick = root_brick
    
    def build_dialogue(self, LLM_Memory, prompt) -> None:
        dialogue = [
            {"role" : "system", "content" : LLM_Memory},
            {"role" : "user", "content" : prompt}
        ]
        return dialogue
    

    def prompt_rendering(self, brick: AgentBrick, mode = "func") -> None:
        if mode == "func":
            back_ground = self.memo("LLM_memory")["LLM_memory"]
            scenario_prompt = brick.back_prompt
            chooies_prompt = [action.front_prompt for action in brick.actions]
            prompt = """"""
            prompt += scenario_prompt + "\n"
            for i, chooies in enumerate(chooies_prompt):
                prompt += f"{i+1}. {chooies}\n"
            
            return back_ground, prompt

        elif mode == "single":
            back_ground = self.memo("LLM_memory")["LLM_memory"]
            scenario_prompt = brick.back_prompt
            prompt = """"""
            prompt += scenario_prompt + "\n"
            return back_ground, prompt
    

    def function_rendering(self, brick: AgentBrick) -> None:
        functions = []
        for action in brick.actions:
            data = {}
            data["name"] = action.brick_name
            data["description"] = action.description
            data["parameters"] = {
                "type" : "object",
                "properties" : action.parameters,
                "required" : list(action.parameters.keys())
            }
            functions.append(data)

        return functions


    def api_func_reply_decode(self, reply: str) -> Dict:
        if "function_call" in reply:
            function_name = reply["function_call"]["name"]
            parameters = reply["function_call"]["arguments"]
            parameters = json.loads(parameters)
            return (function_name, parameters)
        else:
            return ("No_Func", {"ai" : reply["content"]})


    def init_enviroment(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            self.memo.add(key, value)
    

    def show_agent(self):
        pass
        print(self.root_brick.brick_name)

        root_brick = self.root_brick
        for brick in root_brick.actions:
            print(brick.brick_name)
    

    def memo_update(self, mode: str, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            self.memo.update(mode, key, value)


    def run(self, args: Dict) -> None:

        tasks_loop = [(args,self.root_brick)]

        while tasks_loop:
            args, brick = tasks_loop.pop(0)

            if brick.brick_think == "think":
                # think brick, use GPT API to make decision or solve problem

                if brick.action_type == "multi":
                    # use GPT API to make decision
                    llm_memory, prompt = self.prompt_rendering(brick)
                    message = self.build_dialogue(llm_memory, prompt)
                    function_data = self.function_rendering(brick)

                    for i in range(5):
                        try:
                            response = self.gpt_api.query_func(message, function_data)
                            break
                        except:
                            time.sleep(1)
                            i = 999

                    if i == 999:
                        raise Exception("GPT API Error")
                    
                    function_name, parameters =\
                        self.api_func_reply_decode(response)
                    
                    if function_name == "No_Func":
                        raise Exception("GPT API Error, GPT not call any function")
                    
                    # call the next brick
                    for action in brick.actions:
                        if action.brick_name == function_name:
                            next_args = {}
                            for name in action.parameters:
                                if name in parameters:
                                    # use the parameter from GPT First
                                    next_args[name] = parameters[name]
                                else:
                                    next_args[name] = self.memo(name)

                            # pack the next brick and args
                            tasks_loop.append((next_args, action))
                            break

                elif brick.action_type == "single":
                    # use GPT API to solve problem
                    llm_memory, prompt = self.prompt_rendering(brick, mode="single")
                    message = self.build_dialogue(llm_memory, prompt)
                    function_data = self.function_rendering(brick)

                    for i in range(5):
                        try:
                            response = self.gpt_api.query_func(message, function_data, function_call="none")
                        except:
                            time.sleep(1)
                    if i == 4:
                        raise Exception("GPT API Error")
                    
                    _, parameters =\
                        self.api_func_reply_decode(response)
                    
                    action = brick.actions[0]
                    next_args = {}
                    for name in action.parameters:
                        if name in parameters:
                            next_args[name] = parameters[name]
                        else:
                            next_args[name] = self.memo(name)
                    
                    tasks_loop.append((next_args, action))
                    break

            else:
                parameters = {}
                for name in brick.parameters:
                    if name in args:
                        parameters[name] = args[name]
                    else:
                        parameters[name] = self.memo(name)
                
                next_args = brick.call_back(**parameters)

                if brick.action_type == "single":
                    tasks_loop.append((next_args, brick.actions[0]))
                else:
                    self.memo_update("", **next_args)
                    return "FINISH"
                




                


        
    
    



