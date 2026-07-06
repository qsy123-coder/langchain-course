from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.tools import tool
import os
load_dotenv()

@tool
def search (query:str) ->   str:
    """
    Tool that searches over Internet
    Args:
        query:The query to search for
    Returns:
        The search results
    """
    print(f"search for ${query}")
    return "Tokyo's weather is sunny"

llm = ChatOpenAI()
tools=[search]
agent =create_agent(model=llm,tools=tools)

def main():
    print("Hello from langchain-course!")
    result = agent.invoke({"messages":HumanMessage(content="What the weather in tokyo?")})
    print (result)
if __name__ == "__main__":
    main()
