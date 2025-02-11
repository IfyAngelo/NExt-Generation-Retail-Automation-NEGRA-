# from typing import TypeDict, Annotated
# from langgraph.graph.message import add_messages

# # Define the state object for the agent graph
# class AgentGraphState(TypeDict):
#     user_query: str
#     manager_response: Annotated[list, add_messages]
#     sales_agent_response: Annotated[list, add_messages]
#     customer_service_agent_response: Annotated[list, add_messages]
#     items_recommendation_agent_response: Annotated[list, add_messages]
#     # add state objects for tools too
#     cart_agent_response: Annotated[list, add_messages]
#     pos_agent_response: Annotated[list, add_messages]
#     invoice_email_agent_response: Annotated[list, add_messages]
#     end_chain: Annotated[list, add_messages]

# # Define the nodes in the agent graph
# def get_agent_graph_state(state:AgentGraphState, state_key:str):
#     if state_key == "manager_all":
#         return state["manager_response"]
#     elif state_key == "manager_latest":
#         if state["manager_response"]:
#             return state["manager_response"][-1]
#         else:
#             return state["manager_response"]
        
#     elif state_key == "sales_agent_all":
#         return state["sales_agent_response"]
#     elif state_key == "sales_agent_latest":
#         if state["sales_agent_response"]:
#             return state["sales_agent_response"][-1]
#         else:
#             return state["sales_agent_response"]
    
#     elif state_key == "customer_service_agent_all":
#         return state["customer_service_agent_response"][-1]
#     elif state_key == "customer_service_agent_latest":
#         if state["customer_service_agent_response"]:
#             return state["customer_service_agent_response"][-1]
#         else:
#             return state["customer_service_agent_response"]
        
#     elif state_key == "items_recommendation_agent_all":
#         return state["items_recommendation_agent_response"]
#     elif state_key == "items_recommendation_agent_latest":
#         if state["items_recommendation_agent_response"]:
#             return state["items_recommendation_agent_response"][-1]
#         else:
#             return state["items_recommendation_agent_response"]
    
#     # add state nodes for tools too
    
#     elif state_key == "cart_agent_all":
#         return state["cart_agent_response"]
#     elif state_key == "cart_agent_latest":
#         if state["cart_agent_response"]:
#             return state["cart_agent_response"][-1]
#         else:
#             return state["cart_agent_response"]
        
#     elif state_key == "pos_agent_all":
#         return state["pos_agent_response"]
#     elif state_key == "pos_agent_latest":
#         if state["pos_agent_response"]:
#             return state["cart_agent_response"][-1]
#         else:
#             return state["pos_agent_response"]
        
#     elif state_key == "invoice_email_agent_all":
#         return state["invoice_email_agent_response"]
#     elif state_key == "invoice_email_agent_latest":
#         if state["invoice_email_agent_response"]:
#             return state["invoice_email_agent_response"][-1]
#         else:
#             return state["invoice_email_agent_response"]
        
#     else:
#         return None
    
# state = {
#     "user_query":"",
#     "manager_response": [],
#     "sales_agent_response": [],
#     "customer_service_agent_response": [],
#     "items_recommendation_agent_response": [],
#     # add state for tools
#     "cart_agent_response": [],
#     "pos_agent_response": [],
#     "invoice_email_agent_response": [],
#     "end_chain_response": []
# }

# states/states.py
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentGraphState(TypedDict):
    customer_query: str
    customer_complaint: str
    manager_response: Annotated[str, add_messages]
    sales_agent_response: Annotated[str, add_messages]
    customer_service_agent_response: Annotated[str, add_messages]
    items_recommendation_agent_response: Annotated[str, add_messages]
    cart_agent_response: Annotated[str, add_messages]
    pos_agent_response: Annotated[str, add_messages]
    invoice_email_agent: Annotated[str, add_messages]
    end_chain: Annotated[str, add_messages]
    # Additional state fields:
    route: str
    add_to_cart: bool
    checkout: bool
    cart_items: list
    cart_total: int
    payment_status: str
    invoice_email_status: str
    product_info: str
    complaint_info: str
    recommendation: str
    customer_email: str

def get_agent_graph_state(state: AgentGraphState, state_key: str):
    return state.get(state_key, None)

state = {
    "customer_query": "",
    "customer_complaint": "",
    "manager_response": "",
    "sales_agent_response": "",
    "customer_service_agent_response": "",
    "items_recommendation_agent_response": "",
    "cart_agent_response": "",
    "pos_agent_response": "",
    "invoice_email_agent": "",
    "end_chain": "",
    # Additional defaults:
    "route": "sales",
    "add_to_cart": False,
    "checkout": False,
    "cart_items": [],
    "cart_total": 0,
    "payment_status": "",
    "invoice_email_status": "",
    "product_info": "",
    "complaint_info": "",
    "recommendation": "",
    "customer_email": ""
}