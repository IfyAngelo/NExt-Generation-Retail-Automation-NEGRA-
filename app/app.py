# from agent_graph.graph import create_graph, compile_workflow

# # server = 'ollama'
# # model = 'llama3:instruct'
# # model_endpoint = None

# server = 'openai'
# model = 'gpt-4o'
# model_endpoint = None

# # server = 'vllm'
# # model = 'meta-llama/Meta-Llama-3-70B-Instruct' # full HF path
# # model_endpoint = 'https://kcpqoqtjz0ufjw-8000.proxy.runpod.net/' 
# # #model_endpoint = runpod_endpoint + 'v1/chat/completions'
# # stop = "<|end_of_text|>"

# iterations = 40

# print ("Creating graph and compiling workflow...")
# graph = create_graph(server=server, model=model, model_endpoint=model_endpoint)
# workflow = compile_workflow(graph)
# print ("Graph and workflow created.")


# if __name__ == "__main__":

#     verbose = False

#     while True:
#         query = input("Commence Interaction with NEGRA: ")
#         if query.lower() == "exit":
#             break

#         dict_inputs = {"customer_query": query}
#         # thread = {"configurable": {"thread_id": "4"}}
#         limit = {"recursion_limit": iterations}

#         # for event in workflow.stream(
#         #     dict_inputs, thread, limit, stream_mode="values"
#         #     ):
#         #     if verbose:
#         #         print("\nState Dictionary:", event)
#         #     else:
#         #         print("\n")

#         for event in workflow.stream(
#             dict_inputs, limit
#             ):
#             if verbose:
#                 print("\nState Dictionary:", event)
#             else:
#                 print("\n")

# app/app.py
from agent_graph.graph import create_graph, compile_workflow

server = 'openai'
model = 'gpt-4o'
model_endpoint = None
stop = "<|end_of_text|>"
iterations = 40

print("Creating graph and compiling workflow...")
graph = create_graph(server=server, model=model, model_endpoint=model_endpoint, stop=stop)
workflow = compile_workflow(graph)
print("Graph and workflow created.")

if __name__ == "__main__":
    verbose = False
    while True:
        query = input("Commence Interaction with NEGRA: ")
        if query.lower() == "exit":
            break

        # Ask whether the user has a complaint
        complaint = input("If this is a complaint, please enter the complaint details (or leave empty): ")
        # Collect an email address for invoice delivery
        email = input("Enter customer email (for invoice): ")

        dict_inputs = {
            "customer_query": query,
            "customer_complaint": complaint,
            "customer_email": email
        }
        limit = {"recursion_limit": iterations}

        for event in workflow.stream(dict_inputs, limit):
            if verbose:
                print("\nState Dictionary:", event)
            else:
                print("\n")
