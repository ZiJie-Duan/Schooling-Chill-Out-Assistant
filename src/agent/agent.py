from agent.memo import Memo
from agent.gpt_api import GPT_API
from typing import Any, List, Dict
import time
import pprint
import json
import uuid


class AgentBrick:
    """
    AgentBrick serves as the foundational building block in an agent system.
    It represents a callable function that may be invoked by other bricks.

    Args:
    brick_name: A unique identifier for the brick.
    description: A brief summary of the brick's purpose and functionality.
    front_prompt: A guiding prompt aiding higher-level agents in decision making.
    back_prompt: A cue for the subsequent action or scenario.

    brick_think: Defines the operation mode of the brick, either 'think' or 'do'.
        'think': Leverages the language model to ideate.
        'do': Skips the language model thinking process, but triggers the callback function.

    action_type: Specifies the brick's approach to executing actions - 'multi', 'single', 'environment', or 'pop_reply'.
        'multi': Only applicable to 'think' mode. Engages language model to make decisions.
        'single': Applies to either 'think' or 'do' mode. Calls only the subsequent brick.
        'environment': Exclusive to 'do' mode. Saves arguments to memory.
        'pop_reply': Exclusive to 'do' mode. Executes the action and provides a reply.

    actions: A list of bricks that may be invoked by the current brick.
    parameters: A set of parameters required by the brick.
    call_back: A callback function that is triggered when the brick is invoked.

    The parameters for the brick should be defined in the following manner:
    {
        "param_name":{"type": "datatype","description": "brief explanation"},
        "param_name":{"type": "datatype","description": "brief explanation"},
        "param_name":{"type": "datatype", "enum": ["option1", "option2", ...]}
    }
    """

    def __init__(self, 
                brick_name: str = "", # Unique identifier for the brick
                description: str = "", # Summary of the brick's functionality
                front_prompt: str = "",
                back_prompt: str = "",
                brick_think: str = "", # Operation mode of the brick: 'think' or 'do'
                action_type: str = "", # Brick's approach to executing actions: 'multi', 'single', 'environment', or 'pop_reply'
                actions: list = None,
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

    def easy_set_up(self, setting : str, brick_list : List = [], call_back = None) -> None:
        """
        think, do, multi, single, env, popr, nf
        """
        args = setting.split(" ")
        if "think" in args:
            self.brick_think = "think"
        elif "do" in args:
            self.brick_think = "do"
        if "multi" in args:
            self.action_type = "multi"
        elif "single" in args:
            self.action_type = "single"
        elif "env" in args:
            self.action_type = "environment"
        elif "popr" in args:
            self.action_type = "pop_reply"

        if "nf" in args:
            self.call_back = lambda:{}
            
        if "name" in args:
            self.brick_name = args[args.index("name")+1]

        if self.brick_name == "":
            self.brick_name = str(uuid.uuid4())
        if self.description == "":
            self.description = "no description"

        if not self.actions:
            self.actions = []
        for brick in brick_list:

            self.actions.append(brick)
        
        if call_back:
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
    
    def template_rendering(self, back_prompt: str, args: dict) -> None:
        scenario_prompt = back_prompt
        for key, value in args.items():
            scenario_prompt = scenario_prompt.replace(f"{{{key}}}", value)
        return scenario_prompt

    def prompt_rendering(self, brick: AgentBrick, mode = "func", args = {}) -> None:
        if mode == "func":
            back_ground = self.memo("LLM_memory")["LLM_memory"]
            scenario_prompt = self.template_rendering(brick.back_prompt, args)
            chooies_prompt = [action.front_prompt for action in brick.actions]
            prompt = """"""
            prompt += scenario_prompt + "\n"
            for i, chooies in enumerate(chooies_prompt):
                prompt += f"{i+1}. {chooies}\n"
            
            return back_ground, prompt

        elif mode == "single":
            back_ground = self.memo("LLM_memory")["LLM_memory"]
            scenario_prompt = self.template_rendering(brick.back_prompt, args)
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
        self.memo.update(**kwargs)

            
    def get_parameter(self, brick: AgentBrick, args=None) -> Dict:
        if args:
            parameters = {}
            for name in brick.parameters:
                if name in args:
                    parameters[name] = args[name]
                else:
                    parameters[name] = self.memo(name)
            return parameters
        else:
            parameters = {}
            for name in brick.parameters:
                parameters[name] = self.memo(name)
            return parameters
    

    def register(self, env_var) -> None:
        for key, value in env_var.items():
            self.memo.register(key, value)


    def run(self, args: Dict = {}) -> None:

        tasks_loop = [(args,self.root_brick)]
        decision_node = [args,self.root_brick]
        action_chooies = None

        while tasks_loop:
            args, brick = tasks_loop.pop(0)

            if brick.brick_think == "think":
                # think brick, use GPT API to make decision or solve problem

                if brick.action_type == "multi":
                    # use GPT API to make decision
                    llm_memory, prompt = self.prompt_rendering(brick, mode="func", args=args)
                    message = self.build_dialogue(llm_memory, prompt)
                    function_data = self.function_rendering(brick)

                    for i in range(5):
                        try:
                            response = self.gpt_api.query_func(message, function_data)
                            break
                        except:
                            time.sleep(1)
                            i = 999
                        #response = self.gpt_api.query_func(message, function_data)
                        break

                    if i == 999:
                        raise Exception("GPT API Error")
                    
                    function_name, parameters =\
                        self.api_func_reply_decode(response)
                    
                    if function_name == "No_Func":
                        raise Exception("GPT API Error, GPT not call any function")
                    
                    # call the next brick
                    for action in brick.actions:
                        if action.brick_name == function_name:
                            # 疑问，会有参数泄露的问题吗？
                            # 如果不匹配 会怎样？
                            next_args = self.get_parameter(action, parameters)
                            # pack the next brick and args
                            tasks_loop.append((next_args, action))
                            break
                    
                    decision_node = [args,brick] # update decision node
                    action_chooies = action

                elif brick.action_type == "single":
                    # use GPT API to solve problem
                    llm_memory, prompt = self.prompt_rendering(brick, mode="single", args=args)
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
                    next_args = self.get_parameter(action, parameters)
                    tasks_loop.append((next_args, action))
                    break

            else:
                res_args = brick.call_back(**args)
                if not res_args:
                    res_args = {}

                if brick.action_type == "single":
                    next_args = self.get_parameter(brick.actions[0], res_args)
                    tasks_loop.append((next_args, brick.actions[0]))

                elif brick.action_type == "environment":
                    self.memo_update("", **res_args)
                    return "FINISH"
                
                elif brick.action_type == "pop_reply":
                    self.memo_update("", **res_args)

                    history_args = decision_node[0]
                    for k, v in res_args.items():
                        history_args[k] = v

                    next_args = self.get_parameter(decision_node[1], history_args)

                    decision_node[1].actions.remove(action_chooies)
                    decision_node[0] = next_args
                    tasks_loop.insert(0, decision_node)




                


        
    
    



