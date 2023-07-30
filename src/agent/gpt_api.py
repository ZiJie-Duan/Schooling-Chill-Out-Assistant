import openai

class GPT_API:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.model = "gpt-4"  # 设置默认模型

    def set_model(self, model: str):
        self.model = model

    def query(self, 
            messages, 
            temperature = 0.5, 
            max_tokens = 100,
            model = None,
            full = False) -> str:
        
        if not model:
            model = self.model

        response = openai.ChatCompletion.create(
                model = model,
                messages = messages,
                temperature = temperature,
                max_tokens = max_tokens
            )
        if full:
            return response
        else:
            return response.choices[0].message.content


    def query_stream(self, 
            messages, 
            temperature = 0.5, 
            max_tokens = 100,
            model = None,
            full = False) -> str:

        if not model:
            model = self.model
        
        response = openai.ChatCompletion.create(
            model = model,
            messages = messages,
            temperature = temperature,
            max_tokens = max_tokens,
            stream=True,
        )

        if full:
            for chunk in response:
                yield chunk
        
        else:
            for chunk in response:
                word = chunk["choices"][0].get("delta", {}).get("content")
                if word:
                    yield word 
    

    def query_func(self, 
            messages,
            functions,
            temperature = 0.0, 
            max_tokens = 100,
            function_call = "auto",
            model = None) -> str:
        
        print("\n\n\nsend",messages)
        
        if not model:
            model = self.model

        response = openai.ChatCompletion.create(
            model = model,
            messages = messages,
            temperature = temperature,
            max_tokens = max_tokens,
            functions = functions,
            function_call = function_call
        )

        return response["choices"][0]["message"]
