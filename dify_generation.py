import requests
import json


def generate_analysis(user_input, api_key="app-qut6OpoZUdLBuWowxqImw9ks"):
    """
    调用Dify API生成分析结果

    参数:
    user_input (str): 用户输入的文本
    api_key (str): Dify API密钥

    返回:
    dict: 包含所有节点输出的字典
    """
    # API URL
    api_url = "https://api.dify.ai/v1/workflows/run"

    # Request headers
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    # Request payload
    data = {
        "inputs": {"user_input": user_input},
        "response_mode": "streaming",
        "user": "abc-123"
    }

    try:
        # 发送请求并获取流式响应
        response = requests.post(api_url, headers=headers, data=json.dumps(data), stream=True)

        if response.status_code == 200:
            # 提取outputs数据
            outputs = extract_outputs_from_stream(response)
            return outputs
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Error:", response.text)
            return {"error": f"Request failed with status code: {response.status_code}"}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}


def stream_analysis(user_input, api_key="app-qut6OpoZUdLBuWowxqImw9ks"):
    """
    调用Dify API并以流式方式返回分析结果，只输出node_finished事件的outputs
    和text_chunk事件的text

    参数:
    user_input (str): 用户输入的文本
    api_key (str): Dify API密钥

    返回:
    generator: 生成SSE格式的事件流
    """
    # API URL
    api_url = "https://api.dify.ai/v1/workflows/run"

    # Request headers
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    # Request payload
    data = {
        "inputs": {"user_input": user_input},
        "response_mode": "streaming",
        "user": "abc-123"
    }

    try:
        # 发送请求并获取流式响应
        response = requests.post(api_url, headers=headers, data=json.dumps(data), stream=True)

        if response.status_code == 200:
            # 处理流式响应
            for line in response.iter_lines():
                if not line:
                    continue

                # 解码行并去除'data: '前缀
                line_text = line.decode('utf-8').strip()
                if line_text.startswith('data: '):
                    try:
                        json_str = line_text[6:]  # 去掉"data: "前缀
                        event_data = json.loads(json_str)

                        # 提取text_chunk事件的text
                        if event_data.get('event') == 'text_chunk':
                            text = event_data.get('data', {}).get('text', '')
                            if text:
                                yield f"data: {text}\n\n"

                    except json.JSONDecodeError as e:
                        error_msg = json.dumps({"error": f"Error parsing JSON: {str(e)}"})
                        yield f"data: {error_msg}\n\n"
        else:
            error_msg = json.dumps({"error": f"Request failed with status code: {response.status_code}"})
            yield f"data: {error_msg}\n\n"

    except Exception as e:
        error_msg = json.dumps({"error": f"An error occurred: {str(e)}"})
        yield f"data: {error_msg}\n\n"


def extract_outputs_from_stream(response):
    """
    从流式响应中提取node_finished事件的outputs数据

    参数:
    response: 请求的响应对象

    返回:
    dict: 包含所有节点输出的字典
    """
    all_outputs = {}

    # 使用流式处理响应
    for line in response.iter_lines():
        if not line:
            continue

        # 解码行并去除'data: '前缀
        line_text = line.decode('utf-8').strip()
        if line_text.startswith('data: '):
            try:
                json_str = line_text[6:]  # 去掉"data: "前缀
                event_data = json.loads(json_str)

                # 检查是否是node_finished事件
                if event_data.get('event') == 'node_finished':
                    node_id = event_data.get('data', {}).get('node_id', 'unknown')
                    node_outputs = event_data.get('data', {}).get('outputs', {})

                    if node_outputs:
                        # 合并所有节点的outputs，使用节点ID作为键
                        all_outputs[node_id] = node_outputs

                # 也检查workflow_finished事件
                elif event_data.get('event') == 'workflow_finished':
                    workflow_outputs = event_data.get('data', {}).get('outputs', {})
                    if workflow_outputs:
                        all_outputs['workflow'] = workflow_outputs

            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e} - Line: {line_text}")
                continue

    return all_outputs