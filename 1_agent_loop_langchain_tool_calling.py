from langsmith import traceable
from langchain.tools import tool
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage
import os

os.environ["NO_PROXY"] = "localhost,127.0.0.1"
MAX_ITERATIONS=10
MODEL="qwen3:1.7b"
load_dotenv()


@tool
def get_product_price(product:str) -> str:
    """获取产品的原始价格"""
    print(f"  >>excute get_product_price(product:${product})")
    prices={"笔记本电脑":1099.99,"耳机":384.45,"键盘":743.50}
    return prices.get(product,0)

@tool
def apply_discount(price:float,discount_tier:str) -> float:
    """获取折扣后的价格"""
    print(f"   >>excuting apply_discount(prices:${price},dicount_tier:{discount_tier})")
    discount_percentages={"铜牌":5,"银牌":15,"金牌":30}
    discount=discount_percentages.get(discount_tier,0)
    return round((1-discount/100)*price)

# agent loop
@traceable(name="Langchain_Agent_Loop")
def run_agent(question:str):
    tools=[get_product_price,apply_discount]
    tools_dict={t.name:t for t in tools}
    llm=init_chat_model(f"ollama:{MODEL}",temperature=0)
    llm_with_tools=llm.bind_tools(tools)

    print(f"当前的问题是:{question}")
    print("=" * 60)
    messages=[
        SystemMessage(
            content=(
                "你是一名乐于助人的助手,你有权调用get_product_price和apply_discount工具\n"
                "以下是你必须严格遵守的一些规则:\n"
                "1.严禁凭空捏造产品价格，必须调用get_product_price工具获取对应产品价格\n"
                "2.以get_product_price调用返回后的结果作为apply_discount的price参数的输入\n"
                "3.永远不要自己计算折扣"
                "总是使用apply_discount工具"
                "3.严禁凭空捏造折扣等级"
                "4.如果用户没有指定折扣的等级，你需要询问用户折扣的等级是什么(金牌，银牌，铜牌)"
        )),
        HumanMessage(content=question)
    ]

    for iteration in range(1,MAX_ITERATIONS+1):
        print(f"\n--- Iteration{iteration} ---")
        ai_message=llm_with_tools.invoke(messages)
        tool_calls=ai_message.tool_calls

        if not tool_calls:
            print(f"\nFinal answer:{ai_message.content}")
            return ai_message.content
        
        tool_call=tool_calls[0]
        tool_name=tool_call.get("name")
        tool_args=tool_call.get("args",{})
        tool_call_id=tool_call.get("id")
        print(f"  [Tool_Selected]:{tool_name} with args {tool_args}")
        tool_to_use=tools_dict.get(tool_name)

        if tool_to_use is None:
            raise ValueError(f"{tool_name} is not found")
        observation=tool_to_use.invoke(tool_args)
        print(f"   [Tool result]:{observation}")

        messages.append(ai_message)
        messages.append(ToolMessage(content=str(observation),tool_call_id=tool_call_id))

if __name__ == "__main__":
    print("hello from langchain")
    result=run_agent("打过铜牌折扣后的笔记本电脑的价格是多少？")



# from dotenv import load_dotenv

# load_dotenv()

# from langchain.chat_models import init_chat_model
# from langchain.tools import tool
# from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
# from langsmith import traceable

# MAX_ITERATIONS = 10
# MODEL = "qwen2.5:7b"


# # --- Tools (LangChain @tool decorator) ---


# @tool
# def get_product_price(product: str) -> float:
#     """Look up the price of a product in the catalog."""
#     print(f"    >> Executing get_product_price(product='{product}')")
#     prices = {"laptop": 1299.99, "headphones": 149.95, "keyboard": 89.50}
#     return prices.get(product, 0)


# @tool
# def apply_discount(price: float, discount_tier: str) -> float:
#     """Apply a discount tier to a price and return the final price.
#     Available tiers: bronze, silver, gold."""
#     print(f"    >> Executing apply_discount(price={price}, discount_tier='{discount_tier}')")
#     discount_percentages = {"bronze": 5, "silver": 12, "gold": 23}
#     discount = discount_percentages.get(discount_tier, 0)
#     return round(price * (1 - discount / 100), 2)


# # --- Agent Loop ---


# @traceable(name="LangChain Agent Loop")
# def run_agent(question: str):
#     tools = [get_product_price, apply_discount]
#     tools_dict = {t.name: t for t in tools}

#     llm = init_chat_model(f"ollama:{MODEL}", temperature=0)
#     llm_with_tools = llm.bind_tools(tools)

#     print(f"Question: {question}")
#     print("=" * 60)

#     messages = [
#         SystemMessage(
#             content=(
#                 "You are a helpful shopping assistant. "
#                 "You have access to a product catalog tool "
#                 "and a discount tool.\n\n"
#                 "IMPORTANT: Before generating any tool call, you MUST output a brief, plain text paragraph "
#                 "explaining your thought process and what you are about to do. Do NOT use <think> tags, just write it as regular text.\n\n"
#                 "STRICT RULES — you must follow these exactly:\n"
#                 "1. NEVER guess or assume any product price. "
#                 "You MUST call get_product_price first to get the real price.\n"
#                 "2. Only call apply_discount AFTER you have received "
#                 "a price from get_product_price. Pass the exact price "
#                 "returned by get_product_price — do NOT pass a made-up number.\n"
#                 "3. NEVER calculate discounts yourself using math. "
#                 "Always use the apply_discount tool.\n"
#                 "4. If the user does not specify a discount tier, "
#                 "ask them which tier to use — do NOT assume one."
#             )
#         ),
#         HumanMessage(content=question),
#     ]

#     for iteration in range(1, MAX_ITERATIONS + 1):
#         print(f"\n--- Iteration {iteration} ---")

#         ai_message = llm_with_tools.invoke(messages)

#         tool_calls = ai_message.tool_calls

#         # If no tool calls, this is the final answer
#         if not tool_calls:
#             print(f"\nFinal Answer: {ai_message.content}")
#             return ai_message.content

#         # Process only the FIRST tool call — force one tool per iteration
#         tool_call = tool_calls[0]
#         tool_name = tool_call.get("name")
#         tool_args = tool_call.get("args", {})
#         tool_call_id = tool_call.get("id")

#         print(f"  [Tool Selected] {tool_name} with args: {tool_args}")

#         tool_to_use = tools_dict.get(tool_name)
#         if tool_to_use is None:
#             raise ValueError(f"Tool '{tool_name}' not found")

#         observation = tool_to_use.invoke(tool_args)

#         print(f"  [Tool Result] {observation}")

#         messages.append(ai_message)
#         messages.append(
#             ToolMessage(content=str(observation), tool_call_id=tool_call_id)
#         )

#     print("ERROR: Max iterations reached without a final answer")
#     return None


# if __name__ == "__main__":
#     print("Hello LangChain Agent (.bind_tools)!")
#     print()
#     result = run_agent("What is the price of a laptop after applying a gold discount?")