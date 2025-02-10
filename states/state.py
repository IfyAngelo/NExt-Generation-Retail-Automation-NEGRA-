from typing import TypeDict, Annotated
from langgraph.graph.message import add_messages

#Define the state object for the agent graph
class AgentGraphState(TypeDict):
    user_query: str
    manager_response: Annotated[list, add_messages]
    sales_agent_response: Annotated[list, add_messages]
    customer_service_agent_response: Annotated[list, add_messages]
    item_recommendation_agent_response: Annotated[list, add_messages]
    # add states for tools too
    cart_agent_response: Annotated[list, add_messages]
    pos_agent_response: Annotated[list, add_messages]
    invoice_email_agent: Annotated[list, add_messages]


