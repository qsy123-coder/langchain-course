from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
import os
load_dotenv()


def main():
    print("Hello from langchain-course!")
    information = """
    埃隆·里夫·马斯克 FRS（Elon Reeve Musk，1971年6月28日出生）是一位商人，因其对特斯拉（Tesla）、SpaceX、X（前身为推特 Twitter）以及政府效率部（DOGE）的领导而闻名。自2021年以来，马斯克一直是全球首富；截至2025年5月，《福布斯》估计其净资产为4247亿美元。

马斯克出生于南非比勒陀利亚的一个富裕家庭，并于1989年移民加拿大。他于1997年获得宾夕法尼亚大学的学士学位，随后移居美国加利福尼亚州以追求其商业抱负。1995年，马斯克联合创立了软件公司 Zip2。在该公司于1999年被出售后，他联合创立了在线支付公司 X.com，该公司后来合并组建了 PayPal，并于2002年被 eBay 收购。同年，马斯克成为了美国公民。

2002年，马斯克创立了航天技术公司 SpaceX，并担任其首席执行官（CEO）兼首席工程师；此后，该公司在可重复使用火箭和商业航天领域引领了创新。马斯克于2004年作为早期投资者加入了汽车制造商特斯拉，并于2008年成为其首席执行官兼产品架构师；特斯拉此后已成为电动汽车领域的领头羊。2015年，他联合创立了 OpenAI 以推进人工智能（AI）研究，但后来离开；由于对该组织的发展方向以及他们在2020年代 AI 热潮中的领导层日益不满，他成立了 xAI。2022年，他收购了社交网络推特，进行了重大变革并在2023年将其重命名为 X。他的其他业务还包括他在2016年联合创立的神经技术公司 Neuralink，以及他在2017年创立的隧道挖掘公司无聊公司（The Boring Company）。

马斯克是2024年美国总统大选的最大捐赠者，也是全球极右翼人物、事业和政党的支持者。2025年初，他曾担任美国总统唐纳德·特朗普的高级顾问，并成为政府效率部（DOGE）的实际负责人。在与特朗普发生公开争执后，马斯克离开了特朗普政府，并宣布将创建自己的政党——美国党（America Party）。

马斯克的政治活动、观点和言论使他成为一个极具争议的人物，尤其是在 COVID-19 疫情之后。他因发表缺乏科学依据和误导性的言论而受到批评，包括传播关于 COVID-19 的错误信息和宣扬阴谋论，以及对反犹太主义、种族主义和跨性别恐惧症的言论表示赞同。他对推特的收购也引发了争议，因为该平台随后出现了仇恨言论增加和错误信息传播的情况。他在第二届特朗普政府中担任的角色也引发了公众的强烈抵触，尤其是针对政府效率部（DOGE）的反应。
    """

    summary_template = """
    基于 {information} 我想要你创建以下内容:
    1. 简要回答
    2. 关于他的两个有趣事实
    3. 中国人的回应
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(
        temperature=0, 
        base_url="https://api.deepseek.com/v1",       # DeepSeek 官方接口地址
        api_key=os.getenv("DEEPSEEK_API_KEY"),       # 你的官方 sk-xxxx
        model="deepseek-chat"                         # 官方 V3/V4 对话模型代号统一为 deepseek-chat
    )
    
    # llm =ChatOllama(temperature=0,
    #                 model="qwen2.5-coder:7b")
    
    chain = summary_prompt_template | llm

    response = chain.invoke(input={"information": information})
    print(response.content)

if __name__ == "__main__":
    main()