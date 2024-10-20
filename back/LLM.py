from transformers import TextStreamer
from modelscope import AutoModelForCausalLM, AutoTokenizer
import torch
import os
import json
import re

class LLM:
    def __init__(self, model_name = "qwen/Qwen2.5-Coder-1.5B-Instruct"):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,  # 模型路径
            torch_dtype="auto",  # 数据类型自动选择
            device_map="cuda:0",  # 设备自动选择
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
    # 大模型生成代码
    def generate_code(self, prompt):
        messages = [
            {"role": "system", "content": "你是一个智能代码AI助手，负责根据问题完成编码。在编码的过程中，首先给代码文件起一个名字，然后开始正式写代码，在编码过程中适当添加注释。"},  # 系统角色消息
            {"role": "user", "content": prompt},  # 用户角色消息
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,  
            tokenize=False,  
            add_generation_prompt=True, 
        )
        
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        
        streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512,
            streamer=streamer,
        )
        
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return response
    
    # 大模型解析代码
    def extract_code(self, text):
        prompt = f"""
        请从以下全部文本中提取多个代码段并以JSON格式输出，每个代码段应包含语言language、文件路径file_path和代码内容code_content。
        如果没有对应文件路径，请根据对应语言和内容，生成一个文件路径。

        最后返回JSON格式为：
        [
            {{
                "language": "",
                "file_path": "",
                "code_content": ""
            }},
            {{
                "language": "",
                "file_path": "",
                "code_content": ""
            }},
        ]
        
        文本如下：
        '{text}'

        """
        messages = [ {"role": "system", "content": "你是一个智能AI助手，擅长于提取信息"}, {"role": "user", "content": prompt}, ]
        chat = self.tokenizer.apply_chat_template(
            messages,  
            tokenize=False,  
            add_generation_prompt=True,  
        )
        model_inputs = self.tokenizer([chat], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512,
        )

        # 从生成的ID中提取新生成的ID部分
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(f"Code解析已完成。")
        return response
    
    # 保存文件
    def save_code(self, text, root_path):
        pattern = r'```json\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        for i, match in enumerate(matches):
            try:
                json_object = json.loads(match)
                
                for item in json_object:
                    # 获取文件路径
                    file_path = item.get('file_path')  # 直接获取 'file_path' 的值

                    # 如果 file_path 不存在，使用默认文件名
                    if not file_path:
                        file_path = "example.txt"
                    print("file_path:", file_path)
                    
                    # 组合完整的文件路径
                    full_path = os.path.join(root_path, file_path)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, 'w', encoding='utf-8') as file:
                        file.write(item['code_content'])
                
                print(f"文件{full_path}已创建。")   
                
            except json.JSONDecodeError as e:
                print("JSON 解析错误:", match)

            except FileNotFoundError as e:
                print("路径不存在\n", full_path)
