# import os
# import json
# import yaml
# import chainlit as cl
# from chainlit.input_widget import TextInput, Slider, Select, NumberInput
# from agent_graph.graph import create_graph, compile_workflow


# def update_config(openai_llm_api_key, groq_llm_api_key):
#     config_path = "/Users/libertyelectronics/Desktop/langgraph/negra_tool/config/config.yaml"

#     with open(config_path, 'r') as file:
#         config = yaml.safe_load(file)

#     config['OPENAI_API_KEY'] = openai_llm_api_key
#     config['GROQ_API_KEY'] = groq_llm_api_key

#     if openai_llm_api_key:
#         os.environ['OPENAI_API_KEY'] = openai_llm_api_key
#     if groq_llm_api_key:
#         os.environ['GROQ_API_KEY'] = groq_llm_api_key

#     with open(config_path, 'w') as file:
#         yaml.safe_dump(config, file)

#     print("Configuration updated successfully.")

# class ChatWorkflow:
#     def __init__(self):
#         self.workflow = None
#         self.recursion_limit = 40

#     def build_workflow(self, server, model, model_endpoint, temperature, recursion_limit=40, stop=None):
#         graph = create_graph(
#             server=server, 
#             model=model, 
#             model_endpoint=model_endpoint,
#             temperature=temperature,
#             stop=stop
#         )
#         self.workflow = compile_workflow(graph)
#         self.recursion_limit = recursion_limit

#     def invoke_workflow(self, message):
#         if not self.workflow:
#             return "Workflow has not been built yet. Please update settings first."
        
#         dict_inputs = {"customer_query": message.content}
#         limit = {"recursion_limit": self.recursion_limit}
#         reporter_state = None

#         for event in self.workflow.stream(dict_inputs, limit):
#             next_agent = ""
#             if "router" in event.keys():
#                 state = event["router"]
#                 reviewer_state = state['router_response']
#                 # print("\n\nREVIEWER_STATE:", reviewer_state)
#                 reviewer_state_dict = json.loads(reviewer_state)
#                 next_agent_value = reviewer_state_dict["next_agent"]
#                 if isinstance(next_agent_value, list):
#                     next_agent = next_agent_value[-1]
#                 else:
#                     next_agent = next_agent_value

#             if next_agent == "final_report":
#                 # print("\n\nEVENT_DEBUG:", event)
#                 state = event["router"]
#                 reporter_state = state['reporter_response']
#                 if isinstance(reporter_state, list):
#                     print("LIST:", "TRUE")
#                     reporter_state = reporter_state[-1]
#                 return reporter_state.content if reporter_state else "No report available"

#         return "Workflow did not reach final report"

# # Use a single instance of ChatWorkflow
# chat_workflow = ChatWorkflow()

# @cl.on_chat_start
# async def start():
#     await cl.ChatSettings(
#         [
#             Select(
#                 id="server",
#                 label="Select the server you want to use:",
#                 values=[
#                     "openai",
#                     "groq"
#                 ]
#             ),
#             NumberInput(
#                 id="recursion_limit",
#                 label="Enter the recursion limit:",
#                 description="The maximum number of agent actions the workflow will take before stopping. The default value is 40",
#                 initial=40
#             ),
#             TextInput(
#                 id='openai_llm_api_key',
#                 label='Enter your OpenAI API Key:',
#                 description="Only use this if you are using an OpenAI Model.",
#                 # initial="NO_KEY_GIVEN"
#             ),
#             TextInput(
#                 id='groq_llm_api_key',
#                 label='Enter your Groq API Key:',
#                 description="Only use this if you are using Groq.",
#                 # initial="NO_KEY_GIVEN"
#             ),
#             TextInput(
#                 id='stop_token',
#                 label='Stop token:',
#                 description="The token that will be used to stop the model from generating more text. The default value is <|end_of_text|>",
#                 initial="<|end_of_text|>"
#             ),
#             Slider(
#                 id='temperature',
#                 label='Temperature:',
#                 initial=0,
#                 max=1,
#                 step=0.05,
#                 description="Lower values will generate more deterministic responses, while higher values will generate more random responses. The default value is 0"
#             )
#         ]
#     ).send()

# @cl.on_settings_update
# async def update_settings(settings):
#     global author
#     OPENAI_API_KEY = settings["openai_llm_api_key"]
#     GROQ_API_KEY = settings["groq_llm_api_key"]

#     update_config(
#         openai_llm_api_key=OPENAI_API_KEY, 
#         groq_llm_api_key=GROQ_API_KEY,
#         )
    
#     server = settings["server"]
#     model = settings["llm_model"]
#     model_endpoint = settings["server_endpoint"]
#     temperature = settings["temperature"]
#     recursion_limit = settings["recursion_limit"]
#     stop = settings["stop_token"]
#     author = settings["llm_model"]

#     await cl.Message(content="✅ Settings updated successfully, building workflow...").send()
#     chat_workflow.build_workflow(server, model, model_endpoint, temperature, recursion_limit, stop)
#     await cl.Message(content="😊 Workflow built successfully.").send()

# @cl.on_message
# async def main(message: cl.Message):
#     response = await cl.make_async(chat_workflow.invoke_workflow)(message)
#     await cl.Message(content=f"{response}", author=author).send()

# chat/chat.py
import os
import json
import yaml
import chainlit as cl
from chainlit.input_widget import TextInput, Slider, Select, NumberInput
from agent_graph.graph import create_graph, compile_workflow

def update_config(openai_llm_api_key, groq_llm_api_key):
    config_path = "./config/config.yaml"
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    config['OPENAI_API_KEY'] = openai_llm_api_key
    config['GROQ_API_KEY'] = groq_llm_api_key
    if openai_llm_api_key:
        os.environ['OPENAI_API_KEY'] = openai_llm_api_key
    if groq_llm_api_key:
        os.environ['GROQ_API_KEY'] = groq_llm_api_key
    with open(config_path, 'w') as file:
        yaml.safe_dump(config, file)
    print("Configuration updated successfully.")

class ChatWorkflow:
    def __init__(self):
        self.workflow = None
        self.recursion_limit = 40

    def build_workflow(self, server, model, model_endpoint, temperature, recursion_limit=40, stop=None):
        graph = create_graph(
            server=server, 
            model=model, 
            model_endpoint=model_endpoint,
            temperature=temperature,
            stop=stop
        )
        self.workflow = compile_workflow(graph)
        self.recursion_limit = recursion_limit

    async def invoke_workflow(self, message: cl.Message):
        if not self.workflow:
            return "Workflow has not been built yet. Please update settings first."
        
        dict_inputs = {
            "customer_query": message.content,
            "customer_complaint": "",  # For simplicity, no complaint provided in chat
            "customer_email": "customer@example.com"
        }
        limit = {"recursion_limit": self.recursion_limit}
        final_response = None

        for event in self.workflow.stream(dict_inputs, limit):
            if "end_chain" in event:
                final_response = "Transaction complete."
                break
        if not final_response:
            final_response = "Workflow did not complete."
        return final_response

chat_workflow = ChatWorkflow()

@cl.on_chat_start
async def start():
    await cl.ChatSettings(
        [
            Select(
                id="server",
                label="Select the server you want to use:",
                values=["openai", "groq"]
            ),
            NumberInput(
                id="recursion_limit",
                label="Enter the recursion limit:",
                description="The maximum number of agent actions (default 40).",
                initial=40
            ),
            TextInput(
                id='openai_llm_api_key',
                label='Enter your OpenAI API Key:',
                description="(For OpenAI models)"
            ),
            TextInput(
                id='groq_llm_api_key',
                label='Enter your Groq API Key:',
                description="(For Groq models)"
            ),
            TextInput(
                id='stop_token',
                label='Stop token:',
                description="Token to stop generation (default <|end_of_text|>).",
                initial="<|end_of_text|>"
            ),
            Slider(
                id='temperature',
                label='Temperature:',
                initial=0,
                max=1,
                step=0.05,
                description="Lower values = more deterministic responses."
            ),
            TextInput(
                id='llm_model',
                label='LLM Model:',
                description="E.g., gpt-4o"
            ),
            TextInput(
                id='server_endpoint',
                label='Server Endpoint:',
                description="Endpoint for the server, if applicable."
            )
        ]
    ).send()

@cl.on_settings_update
async def update_settings(settings):
    OPENAI_API_KEY = settings["openai_llm_api_key"]
    GROQ_API_KEY = settings["groq_llm_api_key"]

    update_config(openai_llm_api_key=OPENAI_API_KEY, groq_llm_api_key=GROQ_API_KEY)
    
    server = settings["server"]
    model = settings["llm_model"]
    model_endpoint = settings["server_endpoint"]
    temperature = settings["temperature"]
    recursion_limit = settings["recursion_limit"]
    stop = settings["stop_token"]
    await cl.Message(content="✅ Settings updated successfully, building workflow...").send()
    chat_workflow.build_workflow(server, model, model_endpoint, temperature, recursion_limit, stop)
    await cl.Message(content="😊 Workflow built successfully.").send()

@cl.on_message
async def main(message: cl.Message):
    response = await chat_workflow.invoke_workflow(message)
    await cl.Message(content=f"{response}").send()