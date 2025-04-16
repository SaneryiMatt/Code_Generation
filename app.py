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


PREDEFINED_CODE = """// 数据库表结构示例
{
    "users": [
        {"name": "id", "type": "int", "description": "用户ID"},
        {"name": "username", "type": "varchar(255)", "description": "用户名"}
    ],
    "products": [
        {"name": "id", "type": "int", "description": "商品ID"},
        {"name": "price", "type": "decimal(10,2)", "description": "价格"}
    ]
}""".splitlines()  # 按行分割便于流式输出


@app.route("/stream", methods=["POST"])
def stream_endpoint():
    data = request.json
    query = data.get("query", "")

    # 使用LangChain流式处理
    return Response(
        generate_description(query),
        mimetype="text/event-stream"
    )


@app.route("/tables", methods=["POST"])
def tables_endpoint():
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    # 使用LangChain流式处理
    return Response(
        generate_tables(query),
        mimetype="text/event-stream"
    )


@app.route("/dify/stream", methods=["POST"])
def dify_stream_endpoint():
    data = request.json
    query = data.get("query", "")
    print(query)
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # 使用流式响应
    return Response(
        stream_analysis(query),
        mimetype="text/event-stream"
    )


@app.route('/stream/code', methods=["POST"])
def stream_predefined_code():
    data = request.json
    query = data.get("query", "")

    # ✅ 模拟多文件（你也可以改成调用 Dify 或 LangChain 动态生成）
    files = [
        {
            "name": "student.entity.ts",
            "type": "entity",
            "content": """@Entity()
    export class Student {
      @PrimaryGeneratedColumn()
      id: number

      @Column()
      name: string
    }"""
        },
        {
            "name": "student.service.ts",
            "type": "service",
            "content": """@Injectable()
    export class StudentService {
      constructor(
        @InjectRepository(Student)
        private repo: Repository<Student>
      ) {}

      create(data: CreateStudentDto) {
        return this.repo.save(data)
      }
    }"""
        },
        {
            "name": "student.controller.ts",
            "type": "controller",
            "content": """@Controller('students')
    export class StudentController {
      constructor(private readonly service: StudentService) {}

      @Post()
      create(@Body() dto: CreateStudentDto) {
        return this.service.create(dto)
      }
    }"""
        }
    ]

    def generate():
        for file in files:
            yield f"data: {json.dumps(file)}\n\n"
            time.sleep(1.5)  # 模拟生成间隔
        yield "data: [DONE]\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route("/")
def get_index():
    return send_from_directory('static', 'index.html')


# 简单的健康检查端点
@app.route("/health")
def read_root():
    return jsonify({"status": "ok", "message": "LangChain and Dify Streaming API is running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)