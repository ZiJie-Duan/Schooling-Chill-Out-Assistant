from agent.memo import Memo
from agent.gpt_api import GPT_API
from typing import Any, List, Dict
import time
import pprint
import json
import uuid
from functools import wraps
import inspect

# def example_function(param1, param2, param3='default'):
#     pass

# signature = inspect.signature(example_function)

# # 获取参数名
# parameters = [param.name for param in signature.parameters.values()]
# print(parameters)  # 输出 ['param1', 'param2', 'param3']

# # 获取参数的详细信息
# for name, param in signature.parameters.items():
#     print('Name:', name)
#     print('Default value:', param.default)
#     print('Annotation:', param.annotation)
#     print('Kind:', param.kind)
#     print('---------')

# def my_decorator(arg1, arg2):
#     print(f"装饰器参数: {arg1}, {arg2}")

#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             print(f"在函数 {func.__name__} 之前执行，装饰器参数为 {arg1} 和 {arg2}")
#             result = func(*args, **kwargs)
#             print(f"在函数 {func.__name__} 之后执行")
#             return result
#         return wrapper
#     return decorator


# @my_decorator("参数1", "参数2")
# def example_function(param1, param2):
#     print(f"在函数内部：{param1}, {param2}")

# example_function("A", "B")


# def type_classifier(type : any) -> str:
#     pass

# def brick(brick_type : str, envar :any = None) -> object:

#     if brick_type == "think":
#         def decorator(func):
#             ab = AgentBrick(
#                 brick_name = func.__name__,
#                 description = func.__doc__,
#                 brick_think = "think",




#             )

#             @wraps(func)  # 使用 wraps 装饰器
#             def wrapper(*args, **kwargs):
#                 signature = inspect.signature(func)
                
#                 return result
#             return wrapper
    
#     elif brick_type == "do":
#         pass
    
#     return decorator

# @timing_decorator
# def slow_function():
#     """这是一个缓慢的函数"""
#     print("这个函数执行得有点慢...")
#     time.sleep(2)
#     print("函数执行完毕!")

# print(slow_function.__name__)  # 输出 "slow_function"
# print(slow_function.__doc__)   # 输出 "这是一个缓慢的函数"


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
    
    
    def build_dialogue(self, prompt) -> None:
        dialogue = [
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
            scenario_prompt = self.template_rendering(brick.back_prompt, args)
            chooies_prompt = [action.front_prompt for action in brick.actions]
            prompt = ""
            prompt += scenario_prompt + "\n"
            for i, chooies in enumerate(chooies_prompt):
                prompt += f"{i+1}. {chooies}\n"
            
            return prompt

        elif mode == "single":
            scenario_prompt = self.template_rendering(brick.back_prompt, args)
            prompt = ""
            prompt += scenario_prompt + "\n"
            return prompt
    

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
            try:
                parameters = json.loads(parameters)
            except:
                return ("No_Func", {})
            return (function_name, parameters)
        else:
            return ("No_Func", {"ai" : reply["content"]})


    def init_enviroment(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            self.memo.add(key, value)


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
            print("brick name : ",brick.brick_name)

            if brick.brick_think == "think":
                # think brick, use GPT API to make decision or solve problem

                if brick.action_type == "multi":
                    # use GPT API to make decision
                    prompt = self.prompt_rendering(brick, mode="func", args=args)
                    message = self.build_dialogue(prompt)
                    function_data = self.function_rendering(brick)

                    for i in range(5):
                        # try:
                        #     response = self.gpt_api.query_func(message, function_data, max_tokens=2000)
                        #     break
                        # except:
                        #     time.sleep(1)
                        #     i = 999
                        response = self.gpt_api.query_func(message, function_data, max_tokens=2000)
                        break

                    if i == 999:
                        raise Exception("GPT API Error")
                    
                    function_name, parameters =\
                        self.api_func_reply_decode(response)
                    
                    if function_name == "No_Func":
                        print("GPT API Error, GPT not call any function")
                        tasks_loop.append([args, brick])
                        continue
                    
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
                    prompt = self.prompt_rendering(brick, mode="single", args=args)
                    message = self.build_dialogue(prompt)
                    function_data = self.function_rendering(brick)

                    for i in range(5):
                        # try:
                        #     response = self.gpt_api.query_func(message, function_data, max_tokens=2000)
                        #     break
                        # except:
                        #     time.sleep(1)
                        #     i = 999
                        response = self.gpt_api.query_func(message, function_data, max_tokens=2000)
                        break
                    
                    _, parameters =\
                        self.api_func_reply_decode(response)
                    
                    action = brick.actions[0]
                    next_args = self.get_parameter(action, parameters)
                    tasks_loop.append((next_args, action))

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




                


        
    
    



