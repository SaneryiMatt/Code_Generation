from flask import Flask, request, jsonify
from flask_cors import CORS
from LLM import LLM

app = Flask(__name__)
CORS(app)  # 启用跨域

@app.route('/api/chat', methods=['POST'])  
def chat():
    data = request.get_json()  
    #print(data)
    
    system_name = data.get('system_name')
    save_path = data.get('save_path')
    code_language = data.get('code_language')
    description = data.get('description')
    features = data.get('features')

    features_list = []
    for feature in features:
        feature_name = feature.get('feature_name')
        feature_description = feature.get('feature_description')
        features_list.append([feature_name, feature_description])
    
    prompt = f"""请生成一个名为《{system_name}》的软件项目，存储在以下路径：{save_path}。\n代码语言选择为：{code_language}。\n\n 项目介绍：\n{description}\n\n该项目包括以下功能点：\n"""

    for feature in features_list:
        feature_name, feature_description = feature
        prompt += f"- {feature_name}: {feature_description}\n"

    prompt += "\n请确保代码符合最佳实践，并提供相应的注释。生成的代码应包含项目的基本结构，如文件夹和文件的组织。"
    
    llm = LLM()
    ai_response = llm.generate_code(prompt)
    print(ai_response)
    
    print(f"开始解析code")
    text = llm.extract_code(ai_response)
    llm.save_code(text, "example")
    
    return jsonify({'response': ai_response})  # 返回 JSON 响应

if __name__ == '__main__':
    app.run(debug=True)
