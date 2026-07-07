from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from tavily import TavilyClient
from langchain_tavily import TavilySearch
from typing import List
from pydantic import BaseModel,Field
import os
load_dotenv()

tavily=TavilyClient()

class Source(BaseModel):
    """Schema for """
    url:str = Field(description="The URL of the source")

class AgentResponse(BaseModel):
    """"""
    answer: str =Field(description="The answer of the agent to the query")
    source: List[Source] = Field(default_factory=list,description="url list of the answer source")
# @tool
# def search (query:str) ->   str:
#     """
#     Tool that searches over Internet
#     Args:
#         query:The query to search for
#     Returns:
#         The search results
#     """
#     print(f"search for ${query}")
#     return tavily.search(query=query)

llm = ChatOpenAI(temperature=0,base_url="http://api.deepseek.com/v1",api_key=os.getenv("DEEPSEEK_API_KEY"),model="deepseek-chat")
tools=[TavilySearch()]
agent =create_agent(model=llm,tools=tools,response_format=AgentResponse)

def main():
    print("Hello from langchain-course!")
    result = agent.invoke({"messages":HumanMessage(content="洛杉矶的天气如何?")})
    print (result)
if __name__ == "__main__":
    main()
