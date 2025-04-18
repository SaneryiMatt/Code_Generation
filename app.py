from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
from langchain_generation import *
from dify_generation import *
from typing import Iterator
import httpx
import json
from dotenv import load_dotenv

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
    
    if not query:
        return jsonify({"error": "未提供查询"}), 400
    
    try:
        json_result = generate_tables(query)
        tables = json.loads(json_result)
        
        with open("tables.json", "w", encoding="utf-8") as f:
            f.write(json_result)
        
        target_api_url = "http://localhost:5000/api/tables"
        headers = {"Content-Type": "application/json"}
        api_responses = []
        
        for table in tables:
            try:
                response = requests.post(
                    target_api_url,
                    json=table,
                    headers=headers,
                    timeout=10
                )
                if response.status_code >= 200 and response.status_code < 300:
                    api_responses.append({
                        "table": table["name"],
                        "status": "成功",
                        "response": response.json() if response.text else {}
                    })
                else:
                    api_responses.append({
                        "table": table["name"],
                        "status": "失败",
                        "status_code": response.status_code,
                        "response": response.text
                    })
            except requests.RequestException as e:
                api_responses.append({
                    "table": table["name"],
                    "status": "失败",
                    "error": f"请求失败: {str(e)}"
                })
        
        return jsonify({"status": "完成", "responses": api_responses})
        
    except json.JSONDecodeError as e:
        return jsonify({"error": f"JSON格式错误: {str(e)}"}), 500
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
        output_dir = data['output_dir'] if 'output_dir' in data else './'
    
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
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # 使用流式响应
    return Response(
        stream_analysis(query),
        mimetype="text/event-stream"
    )


@app.route("/")
def get_index():
    return send_from_directory('static', 'index.html')

# 简单的健康检查端点
@app.route("/health")
def read_root():
    return jsonify({"status": "ok", "message": "LangChain and Dify Streaming API is running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)