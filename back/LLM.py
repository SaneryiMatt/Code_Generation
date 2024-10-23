from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer


class LLM:
    def __init__(self, model_path='D:\pythonProject\DeepLearning\Qwen2.5-Coder-1.5B-Instruct'):
        self.model_path = model_path
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,  # 模型路径
            torch_dtype="auto",  # 数据类型自动选择
            device_map="auto",  # 设备自动选择
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        
    def generate_code(self, prompt):
        messages = [
            {"role": "system", "content": "你是一个智能代码AI助手，负责根据问题完成编码。"},  # 系统角色消息
            {"role": "user", "content": prompt},  # 用户角色消息
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,  # 要格式化的消息
            tokenize=False,  # 不进行分词
            add_generation_prompt=True,  # 添加生成提示
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

    def generate_code_stream(self, prompt):
        messages = [
            {"role": "system", "content": "你是一个智能代码AI助手，负责根据问题完成编码。"},
            {"role": "user", "content": prompt},
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)

        for generated_ids in self.model.generate(
                model_inputs.input_ids,
                max_new_tokens=512,
                streamer=streamer,
                do_sample=True
        ):
            partial_response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
            yield partial_response
