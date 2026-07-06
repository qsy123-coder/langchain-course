from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from tavily import TavilyClient
from langchain_tavily import TavilySearch
import os
load_dotenv()

tavily=TavilyClient()
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
agent =create_agent(model=llm,tools=tools)

def main():
    print("Hello from langchain-course!")
    result = agent.invoke({"messages":HumanMessage(content="帮我在linkedin上找几个洛杉矶ai工程师的岗位，并列出它们的一些细节?")})
    print (result)
if __name__ == "__main__":
    main()
