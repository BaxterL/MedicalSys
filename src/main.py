from flask import Flask,request,jsonify
from py2neo import Graph
from flask_cors import CORS
from chatnet import ChatBotGraph
import os
from openai import OpenAI
from config import ARK_API_KEY


app = Flask(__name__)
CORS(app)

#doubao-1.5-pro-32k   openai类的一样的自己看着改
client = OpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key
    api_key=ARK_API_KEY,
)

# 连接到Neo4j数据库
url = "bolt://localhost:7687"
username = "neo4j"
password = "password"
graph = Graph(url, auth=(username, password))

handler = ChatBotGraph()

Max_num=200  #可视化界面生成最多的节点数
depth=3      #递归深度

def non_recursive_query(source, n, links):
    stack = [(source, n)]
    visited = set()  # 记录已经访问过的节点

    while stack:
        current_node, depth = stack.pop()

        # 如果当前节点已经访问过或者达到了指定的深度，直接跳过
        if current_node in visited or depth <= 0:
            continue

        # 执行查询
        query = f"""
            MATCH (n {{name: '{current_node}'}})-[r]->(m)
            RETURN n.name AS source, type(r) AS rela, m.name AS target
        """
        result = graph.run(query)
        # 将当前节点标记为已访问
        visited.add(current_node)

        for record in result:
            if len(links) >= Max_num:
                break  # 达到最大节点数，跳出循环
            target = record["target"]
            links.append({
                "source": current_node,
                "rela": record["rela"],
                "target": target
            })
            stack.append((target, depth - 1))

    return links

@app.route('/api/deepseek', methods=['POST'])
def api_deepseek():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "error": "请求参数错误",
                "message": "请提供包含'message'的JSON数据"
            }), 400
        msg = data['message']
        medicalsys_msg = handler.chat_main(msg)
        completion = client.chat.completions.create(
            model="doubao-1-5-pro-32k-character-250715",
            messages=[
                {"role": "system", "content":"你是一个有人情味的智能医疗助手，基于提供的医疗知识图谱系统提供的信息回答问题，可以适当补充，确保专业准确，不编造信息"},
                {"role": "user", "content": f"系统提供的医疗知识：f{medicalsys_msg}\n用户问题：{msg}"}
            ]
        )
        return jsonify({
            "success": True,
            "response": completion.choices[0].message.content
        })
        
    except Exception as e:
        return jsonify({
            "error": "服务器错误",
            "message": str(e)
        }), 500

@app.route('/api/view')
def api_view():
    search_term = request.args.get('search_term', '')
    links = []
    non_recursive_query(search_term, 3, links)
    return jsonify(links)

@app.route('/api/ask',methods=['POST'])
def api_ask():
    msg = request.form.get('msg')
    if msg is None:
        data = request.get_json(silent=True)
        if data and 'msg' in data:
            msg = data['msg']
        else:
            msg = request.args.get('msg')
    if not msg:
        return jsonify({'msg': '', 'res': '未收到问题内容'}), 400
    res = handler.chat_main(msg)
    return jsonify({
        'success': True,
        'msg': msg,
        'res': res
    }), 200

if __name__ == '__main__':
    # test = []
    # non_recursive_query("晕厥",3,test)
    # print(test)
    app.run(debug=True, host='0.0.0.0', port=5000)