from flask import Flask, request, jsonify
from flask_cors import CORS
from LLM import LLM

app = Flask(__name__)
CORS(app)  # 启用跨域

@app.route('/api/chat', methods=['POST'])  # 确保这里的路径和方法正确
def chat():
    data = request.get_json()  # 获取 JSON 数据
    prompt = data.get('message')  # 从请求中获取消息
    
    llm = LLM()
    ai_response = llm.generate_code(prompt)
    print(ai_response)
    
    return jsonify({'response': ai_response})  # 返回 JSON 响应

if __name__ == '__main__':
    app.run(debug=True)
