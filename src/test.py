
from langchain.prompts import PromptTemplate


from langchain.chat_models import ChatOpenAI
chat_model = ChatOpenAI()

pp = PromptTemplate.from_template("Say {foo}")
print(pp.format(foo="bar"))
print(pp.format(foo="bar2"))
print(pp.format(foo="bar3"))