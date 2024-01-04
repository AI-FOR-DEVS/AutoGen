from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json
from search import search, search_declaration

assistant = AssistantAgent('assistant', llm_config={"functions": [search_declaration], "config_list": config_list_from_json("OAI_CONFIG_LIST")})

user_proxy = UserProxyAgent('user_proxy', function_map={"Search": search})

llm_config = {"config_list": config_list_from_json("OAI_CONFIG_LIST")}

cynic = AssistantAgent('cynic', system_message="You are a cynic and you comment everything", llm_config=llm_config)

groupchat = GroupChat(agents=[assistant, cynic, user_proxy], messages=[])

groupchat_manager = GroupChatManager(groupchat, llm_config=llm_config)

user_proxy.initiate_chat(groupchat_manager, message="Find the latest stock price of Apple")