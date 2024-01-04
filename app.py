# Step 1: Import necessary libraries for AutoGen and other functionalities.
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json
from search import search, search_declaration

# Step 2: Set up the AssistantAgent with appropriate configuration to handle tasks and queries.

assistant = AssistantAgent('assistant', llm_config={"functions": [search_declaration], "config_list": config_list_from_json("OAI_CONFIG_LIST")})

# Step 3: Define a UserProxyAgent which acts as an intermediary between the user and the assistant, configuring it for code execution and user interaction modes.

user_proxy = UserProxyAgent('user_proxy', function_map={"Search": search})

llm_config = {"config_list": config_list_from_json("OAI_CONFIG_LIST")}

cynic = AssistantAgent('cynic', system_message="You are a cynic and you comment everything", llm_config=llm_config)

groupchat = GroupChat(agents=[assistant, cynic, user_proxy], messages=[])

groupchat_manager = GroupChatManager(groupchat, llm_config=llm_config)

# Step 4: Initiate a conversation between the user proxy and the assistant agent, starting with a specific task like sentiment analysis or data retrieval.

user_proxy.initiate_chat(groupchat_manager, message="Find the latest stock price of Apple")