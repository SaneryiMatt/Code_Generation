from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser
from typing import Iterator
import time


def generate_description(query: str) -> Iterator[str]:
    # 创建支持流式输出的模型
    chat = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            streaming=True
    )
    
    # 使用正确的消息格式 - 使用字典而不是元组
    prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": "{text}"},
            {"role": "human", "content": "{input}"}
    ])

    output_parser = StrOutputParser()

    # 系统提示内容
    text = """
```xml
<instruction>
<task_description>
你的任务是需求润色，负责生成一个模块中包含哪些信息，以及信息的字段。
</task_description>

<instructions>
1. 请根据输入的要求，创建一个模块名称，并包含以下信息字段。
2. 每个信息字段后面用括号列出具体的属性，如姓名、学号、性别等。
3. 确保每个信息字段都有清晰明了的属性描述，以便后续使用。
4. 输出时，请不要包含任何xml标签，只需列出信息模块及其对应的属性字段。

<examples>
例1：
输入：
创建一个图书管理模块，包含：
1. 书籍信息
2. 作者信息
3. 出版社信息

输出：
图书管理模块：
1. 书籍信息（书名、ISBN、作者、出版社、出版日期、价格、库存、备注）
2. 作者信息（姓名、国籍、生日、作品数量、备注）
3. 出版社信息（名称、地点、联系方式、成立时间、备注）

例2：
输入：
创建一个健康管理模块，包含：
1. 患者信息
2. 医生信息
3. 就诊记录

输出：
健康管理模块：
1. 患者信息（姓名、性别、年龄、联系方式、病史、过敏史、家庭地址、状态、备注）
2. 医生信息（姓名、科室、职称、工作时间、联系方式、状态、备注）
3. 就诊记录（患者姓名、医生姓名、就诊时间、症状描述、诊断结果、处方、状态、备注）

例3：
输入：
创建一个项目管理模块，包含：
1. 项目信息
2. 团队信息
3. 任务信息

输出：
项目管理模块：
1. 项目信息（项目名称、负责人、开始日期、结束日期、状态、备注）
2. 团队信息（团队名称、团队成员、团队领导、创建日期、状态、备注）
3. 任务信息（任务名称、负责人、截止日期、优先级、状态、备注）
</examples>
"""
    # 创建链
    chain = prompt | chat | output_parser

    try:
        for chunk in chain.stream({"text": text, "input": query}):
            if hasattr(chunk, 'content') and chunk.content:
                yield f"data: {chunk.content}\n\n"
            time.sleep(0.01)
        yield "data: [DONE]\n\n"
    except Exception as e:
        print(f"Error in generate_stream: {str(e)}")
        yield f"data: Error: {str(e)}\n\n"
        yield "data: [DONE]\n\n"
