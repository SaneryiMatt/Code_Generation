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
CORS(app)  # 配置CORS，允许前端访问

def dify_stream(query: str) -> Iterator[str]:
    """
    使用Dify API生成流式响应的生成器，并提取文本内容
    """
    # 准备发送到Dify API的请求数据
    dify_data = {
        "inputs": {
            "user_input": query 
        },
        "response_mode": "streaming",
        "user": "user-flask"  # 用户标识
    }
    
    headers = {
        'Authorization': 'Bearer app-qut6OpoZUdLBuWowxqImw9ks',
        'Content-Type': 'application/json'
    }
    
    # 是否在thinking模式中
    in_thinking = False
    
    try:
        with httpx.Client() as client:
            with client.stream("POST", "https://api.dify.ai/v1/workflows/run", json=dify_data, headers=headers) as response:
                if response.status_code != 200:
                    # 读取错误响应内容
                    error_content = b''
                    for chunk in response.iter_bytes():
                        error_content += chunk
                    
                    error_msg = f"Error from Dify API: {response.status_code} - {error_content.decode('utf-8')}"
                    print(error_msg)
                    yield f"data: {error_msg}\n\n"
                    yield "data: [DONE]\n\n"
                    return
                
                # 流式传输响应
                for chunk in response.iter_lines():
                    if not chunk:
                        continue
                        
                    # 确保chunk是字符串
                    if isinstance(chunk, bytes):
                        chunk_str = chunk.decode('utf-8')
                    else:
                        chunk_str = str(chunk)
                    
                    # 去掉可能存在的"data: "前缀
                    if chunk_str.startswith('data: '):
                        chunk_str = chunk_str[6:]
                    
                    try:
                        # 解析JSON数据
                        json_data = json.loads(chunk_str)
                        
                        # 提取文本块事件
                        if json_data.get("event") == "text_chunk":
                            text = json_data.get("data", {}).get("text", "")
                            
                            # 检查是否是thinking模式
                            if text.startswith("<think"):
                                in_thinking = True
                                # 可选：输出thinking的开始标记
                                print("<thinking>")
                                # 继续发送thinking内容
                                yield f"data: {text}\n\n"
                            elif text.endswith("</think>"):
                                in_thinking = False
                                # 可选：输出thinking的结束标记
                                print("</thinking>")
                                # 继续发送thinking内容
                                yield f"data: {text}\n\n"
                            else:
                                # 正常文本内容
                                yield f"data: {text}\n\n"
                        # 可以根据需要处理其他事件类型
                        elif json_data.get("event") == "workflow_finished":
                            # 工作流结束事件
                            yield "data: [DONE]\n\n"
                    except json.JSONDecodeError:
                        # 非JSON格式的行，直接传递
                        yield f"data: {chunk_str}\n\n"
                
                # 确保结束标记
                yield "data: [DONE]\n\n"
    except Exception as e:
        print(f"Error in dify_stream: {str(e)}")
        yield f"data: Error: {str(e)}\n\n"
        yield "data: [DONE]\n\n"

@app.route("/stream", methods=["POST"])
def stream_endpoint():
    data = request.json
    query = data.get("query", "")
    
    # 使用LangChain流式处理
    return Response(
        generate_description(query),
        mimetype="text/event-stream"
    )

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