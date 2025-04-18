from flask import Flask, request, jsonify, Response, send_from_directory, stream_with_context
from flask_cors import CORS
from langchain_generation import *
from dify_generation import *
from typing import Iterator
import httpx
import json
from dotenv import load_dotenv
import time
import requests
# 加载环境变量
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route("/stream", methods=["POST"])
def stream_endpoint():
    data = request.json
    query = data.get("query", "")
    
    return Response(
        generate_description(query),
        mimetype="text/event-stream"
    )


@app.route("/tables", methods=["POST"])
def tables_endpoint():
    data = request.json
    query = data.get("query", "")
    print(f"[DEBUG] 接收到 tables 请求，query: {query}")
    if not query:
        return jsonify({"error": "未提供查询"}), 400

    try:
        # 1. 表结构生成
        json_result = generate_tables(query)
        print(f"[DEBUG] 表结构 JSON: {json_result}")
        tables = json.loads(json_result)

        # 2. 转发给另一个后端用于页面生成
        target_api_url = "http://localhost:5000/api/tables/"
        headers = {"Content-Type": "application/json"}

        for table in tables:
            try:
                print(f"[DEBUG] 发送表结构到：{target_api_url}")
                print(f"[DEBUG] 表数据: {json.dumps(table, ensure_ascii=False)}")
                response = requests.post(target_api_url, json=table, headers=headers, timeout=10)
                print(f"[DEBUG] 创建表 `{table['name']}` 响应：{response.status_code} {response.text}")
            except Exception as e:
                print(f"[ERROR] 创建表 `{table['name']}` 请求失败: {e}")

        # 3. 生成代码文件（调用 /code）
        code_res = requests.post("http://localhost:8000/code", json={
            "json_data": tables,
            "output_dir": "./generated_code"
        })
        print("[DEBUG] /code 返回：", code_res.text)

        return jsonify({
            "status": "success",
            "message": "表结构生成并已转发 & 代码已保存",
            "tables": tables,
            "code": code_res.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/code", methods=["POST"])
def code_endpoint():
    try:
        # 获取请求中的 JSON 数据
        data = request.get_json()
        if not data or 'json_data' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'json_data' in request body"
            }), 400
        
        json_data = data['json_data']
        output_dir =  'E:/desktop/BigCreate/test_branch/Code_Generation-test/backend'
    
        # 调用保存代码函数
        saved_files = save_code_to_local(json_data, output_dir)
        
        return jsonify({
            "status": "success",
            "saved_files": saved_files,
            "message": "Code generated and saved successfully"
        }), 200
    
    except FileNotFoundError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to generate or save code: {str(e)}"
        }), 500
    

@app.route("/dify/stream", methods=["POST"])
def dify_stream_endpoint():
    data = request.json
    query = data.get("query", "")
    print(f"[DEBUG] 接收到 读取文件 请求，query: {query}")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # 使用流式响应
    return Response(
        stream_analysis(query),
        mimetype="text/event-stream"
    )


@app.route("/stream/files", methods=["POST"])
def stream_files():
    folder = "E:/desktop/BigCreate/test_branch/Code_Generation-test/backend/model"  # 根据 code 生成落盘路径
    paths = [os.path.join(folder, f) for f in os.listdir(folder)
             if f.endswith((".py", ".ts", ".js"))]
    print(paths)
    def generate():
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"[ERROR] 读取文件失败: {path} -> {e}")
            filename = os.path.basename(path)
            file_data = {
                "name": filename,
                "type": "python" if filename.endswith(".py") else "typescript",
                "content": content
            }
            yield f"data: {json.dumps(file_data, ensure_ascii=False)}\n\n"
            time.sleep(0.8)  # 控制打字速度
        yield "data: [DONE]\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route("/")
def get_index():
    return send_from_directory('static', 'index.html')

# 简单的健康检查端点
@app.route("/health")
def read_root():
    return jsonify({"status": "ok", "message": "LangChain and Dify Streaming API is running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)