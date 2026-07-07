from langsmith import traceable
from langchain.tools import tool
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage
import os

MAX_ITERATIONS=10
MODEL="qwen2.5-coder:7b"
load_dotenv()


@tool
def get_product_price(product:str) -> str:
    """获取产品的价格"""
    print(f"  >>excute get_product_price(product:${product})")
    prices={"laptop":1099.99,"headphones":384.45,"keyboard":743.50}
    return prices.get(product,0)

@tool
def apply_discount(price:float,discount_tier:str) -> float:
    """获取折扣后的价格"""
    print(f"   >>excuting apply_discount(prices:${price},dicount_tier:${discount_tier})")
    discount_percentages={"bronze":5,"sliver":15,"gold":30}
    discount=discount_percentages.get(discount_tier,0)
    return round((1-discount/100)*price)

# agent loop
@traceable(name="Langchain_Agent_Loop")
def run_agent(question:str):
    tools=[get_product_price,apply_discount]
    tools_dict={t.name:t for t in tools}
    


if __name__ == "__main__":
    print("hello from langchain")
    run_agent("打过折后的产品的价格是多少？")
