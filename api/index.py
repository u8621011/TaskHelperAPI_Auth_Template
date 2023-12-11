from flask import Flask, Response, request, jsonify
import os
from flask_cors import CORS
from .auth import get_user_info_from_token


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://chat.openai.com", "https://chat.openai.com"]}})  # 允許 chatgpt 的 CORS 請求


# 保存 todo 的地方，當 python 案例重啟後就會消失。
_TODOS = {}

@app.route("/todos/<string:username>", methods=['POST'])
def add_todo(username):
    # 我們其實拿不到 username, 使用 OAuth 得到的 user_id 來當作 key
    (user_id, plan_id, name, email) = get_user_info_from_token()

    data = request.get_json(force=True)
    todo = data["todo"]

    if user_id not in _TODOS:
        _TODOS[user_id] = []
    _TODOS[user_id].append(todo)

    return 'OK', 200

@app.route("/todos/<string:username>", methods=['GET'])
def get_todos(username):
    # 我們其實拿不到 username, 使用 OAuth 得到的 user_id 來當作 key
    (user_id, plan_id, name, email) = get_user_info_from_token()

    return jsonify(_TODOS.get(user_id, []))

# ChatGPT 目前並不支援 DELETE。使用 HTTP DELETE 會失敗，改用 POST 來 workaround
#@app.route("/todos/<string:username>", methods=['DELETE'])
#def delete_todo(username):
@app.route("/todos/cancel/<string:username>", methods=['POST'])
def cancel_todo(username):
    # 我們其實拿不到 username, 使用 OAuth 得到的 user_id 來當作 key
    (user_id, plan_id, name, email) = get_user_info_from_token()

    data = request.get_json(force=True)
    todo_idx = data["todo_idx"]

    # fail silently, it's a simple plugin
    if 0 <= todo_idx < len(_TODOS[user_id]):
        _TODOS[user_id].pop(todo_idx)
        
    return 'OK', 200


@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'