from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Iterator, List
import json
import os
import re


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
2. 每个信息字段后面用括号列出具体的属性，但属性个数不超过6个，如姓名、学号、性别等，不包括id字段和备注字段等无关信息。
3. . 输出时，请不要包含任何xml标签，只需列出信息模块及其对应的属性字段。

<examples>
例1：
输入：
创建一个图书管理模块，包含：
1. 书籍信息
2. 作者信息
3. 出版社信息

输出：
图书管理模块：
1. 书籍信息（书名、ISBN、作者、出版社、出版日期、价格、库存）
2. 作者信息（姓名、国籍、生日、作品数量）
3. 出版社信息（名称、地点、联系方式、成立时间）

例2：
输入：
创建一个健康管理模块，包含：
1. 患者信息
2. 医生信息
3. 就诊记录

输出：
健康管理模块：
1. 患者信息（姓名、性别、年龄、联系方式、病史、过敏史、家庭地址、状态）
2. 医生信息（姓名、科室、职称、工作时间、联系方式、状态）
3. 就诊记录（患者姓名、医生姓名、就诊时间、症状描述、诊断结果、处方、状态）

例3：
输入：
创建一个项目管理模块，包含：
1. 项目信息
2. 团队信息
3. 任务信息

输出：
项目管理模块：
1. 项目信息（项目名称、负责人、开始日期、结束日期、状态）
2. 团队信息（团队名称、团队成员、团队领导、创建日期、状态）
3. 任务信息（任务名称、负责人、截止日期、优先级、状态）
</examples>
"""
    # 创建链
    chain = prompt | chat | output_parser

    try:
        for chunk in chain.stream({"text": text, "input": query}):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        print(f"Error in generate_stream: {str(e)}")
        yield f"data: Error: {str(e)}\n\n"
        yield "data: [DONE]\n\n"



def generate_tables(query: str) -> Iterator[str]:
    chat = ChatOllama(
        model="deepseek-r1:14b",
        base_url="http://10.126.59.25:11434", 
        temperature=0,
        num_predict=-1,
    )

    # 使用正确的消息格式 - 使用字典而不是元组
    prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": "{text}"},
            {"role": "human", "content": "{input}"}
    ])

    output_parser = JsonOutputParser()

    chain = prompt | chat | output_parser

    text = """
```xml
<instruction>
<instructions>
1. 根据需求生成对应表设计，并按照JSON格式严格输出。
2. 严格遵守要求生成的fields只能包括以下类型：text、longtext、number、integer、date、datetime、boolean。
3. 生成内容中description不能为空。
4. 严格按照需求，要多少个信息，设计多少个表单。
5. 输出不应包含任何xml标记。

<example>
input:
图书管理模块：
1. 书籍信息（书名、ISBN、作者、出版社、出版日期、价格、库存）
2. 作者信息（姓名、国籍、生日、作品数量）
3. 出版社信息（名称、地点、联系方式、成立时间）

output:
[
{
    "name": "books",
    "display_name": "书籍",
    "description": "这个是一个书籍信息表",
    "fields": [
        {
            "name": "name",
            "display_name": "书名",
            "field_type": "text",
            "required": true,
            "default_value": ""
        },
        {
            "name": "ISBN",
            "display_name": "ISBN",
            "field_type": "text",
            "required": true,
            "default_value": ""
        }
    ]
},
{
    "name": "author",
    "display_name": "作者",
    "description": "这是一个作者信息表",
    "fields": [
        {
            "name": "name",
            "display_name": "书名",
            "field_type": "text",
            "required": true,
            "default_value": ""
        },
        {
            "name": "nation",
            "display_name": "国籍",
            "field_type": "text",
            "required": false,
            "default_value": ""
        }
    ]
},
]

<example>
input:
学生信息管理系统：
1. 学生信息（姓名、学号、性别、年龄、班级、联系方式）
2. 班级信息（班级名称、班主任、学生人数）

output:
[
{
    "name": "student",
    "display_name": "学生",
    "description": "这个学生信息表",
    "fields": [
        {
            "name": "name",
            "display_name": "姓名",
            "field_type": "text",
            "required": true,
            "default_value": ""
        },
        {
            "name": "student_id",
            "display_name": "学号",
            "field_type": "text",
            "required": true,
            "default_value": ""
        }
    ]
},
{
    "name": "class",
    "display_name": "班级",
    "description": "这是一个班级信息表",
    "fields": [
        {
            "name": "class_name",
            "display_name": "班级名称",
            "field_type": "text",
            "required": true,
            "default_value": ""
        },
        {
            "name": "class_teacher",
            "display_name": "班主任",
            "field_type": "text",
            "required": true,
            "default_value": ""
        }
    ]
},
]

<example>
input:
餐厅管理系统：
1. 菜品信息（菜名、价格、口味、烹饪时间）
2. 厨师信息（姓名、工龄、擅长菜系、联系方式）

output:
[
{
    "name": "dish",
    "display_name": "菜品",
    "description": "这是一个菜品信息表",
    "fields": [
        {
            "name": "dish_name",
            "display_name": "菜名",
            "field_type": "text",
            "required": true,
            "default_value": ""
        },
        {
            "name": "price",
            "display_name": "价格",
            "field_type": "text",
            "required": true,
            "default_value": ""
        }
    ]
},
{
    "name": "chef",
    "display_name": "厨师",
    "description": "这是一个厨师信息表",
    "fields": [
        {
            "name": "name",
            "display_name": "姓名",
            "field_type": "text",
            "required": true,
            "default_value": ""
        },
        {
            "name": "years_of_experience",
            "display_name": "工龄",
            "field_type": "text",
            "required": true,
            "default_value": ""
        }
    ]
},
]
```
"""

    result = chain.invoke({"text": text, "input": query})

    return json.dumps(result, ensure_ascii=False, indent=2)


def generate_code(json_data: str) -> Iterator[tuple[str, str]]:
    # 初始化聊天模型
    chat = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            streaming=True
    )

    # 读取 prompt 文件
    try:
        with open('code_prompt.txt', 'r', encoding='utf-8') as file:
            prompt_template = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("Prompt file 'code_prompt.txt' not found")

    # 创建 PromptTemplate
    prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": "{text}"},
            {"role": "human", "content": "{json_data}"}
    ])
    
    # 创建链
    chain = prompt | chat | StrOutputParser()

    # 调用链生成代码
    response = chain.invoke({"text": prompt_template, "json_data": json_data})
    print(response)
    
    # 正则表达式匹配文件路径和代码块
    # 匹配格式：# model/table_name.py \n ``` \n code \n ```
    pattern = r'#\s*(model/[\w/]+\.py)\s*\n```(?:python)?\n(.*?)```'
    matches = re.findall(pattern, str(response), re.DOTALL)
    
    # 迭代返回每个文件路径和代码块
    for file_path, code in matches:
        yield file_path, code.strip()

def save_code_to_local(json_data: str, output_dir: str = "./") -> list[str]:
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    saved_files = []
    
    try:
        for file_path, code in generate_code(json_data):
            full_path = os.path.join(output_dir, file_path)
            print(full_path)
            
            # 确保文件目录存在
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # 保存代码到文件
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(code)
            saved_files.append(full_path)
    except Exception as e:
        raise Exception(f"Error saving code: {str(e)}")
    
    return saved_files