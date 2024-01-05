from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json
from search import search, search_declaration
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socket_io = SocketIO(app)

def new_print_received_message(self, message, sender):
    print(f"PATCHED {sender.name}: {message.get('content')}")
    socket_io.emit('message', {"sender": sender.name, "content": message.get('content')})

GroupChatManager._print_received_message = new_print_received_message

assistant = AssistantAgent('assistant', llm_config={"functions": [search_declaration], "config_list": config_list_from_json("OAI_CONFIG_LIST")})

def is_termination_msg(data):
    has_content = "content" in data and data["content"] is not None
    return has_content and "TERMINATE" in data["content"]

user_proxy = UserProxyAgent('user_proxy', is_termination_msg=is_termination_msg, human_input_mode='NEVER', function_map={"Search": search})

llm_config = {"config_list": config_list_from_json("OAI_CONFIG_LIST")}

cynic = AssistantAgent('cynic', system_message="You are a cynic and you comment everything", llm_config=llm_config)

groupchat = GroupChat(agents=[assistant, cynic, user_proxy], messages=[])

groupchat_manager = GroupChatManager(groupchat, llm_config=llm_config)

@app.route('/run')
def run():
    stockname = request.args.get('stock')
    user_proxy.initiate_chat(groupchat_manager, message=f"Find the latest stock price of {stockname}")

    messages = user_proxy.chat_messages[groupchat_manager]
    return jsonify(messages)

@app.route('/')
def index():
    return render_template('index.html')

app.run(debug=True, port=8080)