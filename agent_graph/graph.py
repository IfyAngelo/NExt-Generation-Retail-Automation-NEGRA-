# import json
# import ast
# from langchain_core.runnables import RunnableLambda
# from langgraph.graph import StateGraph, END
# from typing import TypedDict, Annotated
# from langchain_core.messages import HumanMessage
# from models.openai_models import get_open_ai_json
# from langgraph.checkpoint.sqlite import SqliteSaver
# from agents.agents import (
#     ManagerAgent,
#     SalesAgent,
#     CustomerServiceAgent,
#     ItemsRecommendationAgent,
#     CartAgent,
#     POSAgent,
#     InvoiceEmailAgent,
#     EndNodeAgent
# )
# from prompts.prompts import (
#     manager_prompt_template,
#     salesagent_prompt_template, 
#     customerserviceagent_prompt_template, 
#     itemsrecommendationagent_prompt_template, 
#     cartagent_prompt_template,
#     posagent_prompt_template,
#     invoiceemailer_prompt_template,
#     manager_guided_json,
#     salesagent_guided_json,
#     itemsrecommendationagent_guided_json,
#     customerserviceagent_guided_json,
#     cartagent_guided_json,
#     pos_guided_json,
#     invoiceemailer_guided_json

# )
# from tools.google_serper import get_google_serper
# from tools.basic_scraper import scrape_website
# from states.state import AgentGraphState, get_agent_graph_state, state

# def create_graph(server=None, model=None, stop=None, model_endpoint=None, temperature=0):
#     graph = StateGraph(AgentGraphState)

#     graph.add_node(
#         "manager", 
#         lambda state: ManagerAgent(
#             state=state,
#             model=model,
#             server=server,
#             guided_json=manager_guided_json,
#             stop=stop,
#             model_endpoint=model_endpoint,
#             temperature=temperature
#         ).invoke(
#             customer_query=state["customer_query"],
#             feedback=lambda: get_agent_graph_state(state=state, state_key="reviewer_latest"),
#             # previous_plans=lambda: get_agent_graph_state(state=state, state_key="planner_all"),
#             prompt=manager_prompt_template
#         )
#     )

#     graph.add_node(
#         "salesagent",
#         lambda state: SalesAgent(
#             state=state,
#             model=model,
#             server=server,
#             guided_json=salesagent_guided_json,
#             stop=stop,
#             model_endpoint=model_endpoint,
#             temperature=temperature
#         ).invoke(
#             customer_query=state["customer_query"],
#             feedback=lambda: get_agent_graph_state(state=state, state_key="reviewer_latest"),
#             previous_query=lambda: get_agent_graph_state(state=state, state_key="sales_agent_all"),
#             # serp=lambda: get_agent_graph_state(state=state, state_key="serper_latest"),
#             prompt=salesagent_prompt_template,
#         )
#     )

#     graph.add_node(
#         "customerserviceagent", 
#         lambda state: CustomerServiceAgent(
#             state=state,
#             model=model,
#             server=server,
#             guided_json=customerserviceagent_guided_json,
#             stop=stop,
#             model_endpoint=model_endpoint,
#             temperature=temperature
#         ).invoke(
#             customer_complaint=state["customer_complaint"],
#             feedback=lambda: get_agent_graph_state(state=state, state_key="reviewer_latest"),
#             previous_complaints=lambda: get_agent_graph_state(state=state, state_key="reporter_all"),
#             # research=lambda: get_agent_graph_state(state=state, state_key="scraper_latest"),
#             prompt=customerserviceagent_prompt_template
#         )
#     )

#     graph.add_node(
#         "itemsrecommender", 
#         lambda state: ItemsRecommendationAgent(
#             state=state,
#             model=model,
#             server=server,
#             guided_json=itemsrecommendationagent_guided_json,
#             stop=stop,
#             model_endpoint=model_endpoint,
#             temperature=temperature
#         ).invoke(
#             customer_query=state["customer_query"],
#             feedback=lambda: get_agent_graph_state(state=state, state_key="reviewer_all"),
#             # planner=lambda: get_agent_graph_state(state=state, state_key="planner_latest"),
#             # selector=lambda: get_agent_graph_state(state=state, state_key="selector_latest"),
#             recommender=lambda: get_agent_graph_state(state=state, state_key="reporter_latest"),
#             # planner_agent=planner_prompt_template,
#             # selector_agent=selector_prompt_template,
#             # reporter_agent=reporter_prompt_template,
#             # serp=lambda: get_agent_graph_state(state=state, state_key="serper_latest"),
#             prompt=itemsrecommendationagent_prompt_template
#         )
#     )

#     graph.add_node(
#         "cartagent", 
#         lambda state: CartAgent(
#             state=state,
#             model=model,
#             server=server,
#             guided_json=cartagent_guided_json,
#             stop=stop,
#             model_endpoint=model_endpoint,
#             temperature=temperature
#         ).invoke(
#             customer_query=state["customer_query"],
#             feedback=lambda: get_agent_graph_state(state=state, state_key="reviewer_all"),
#             # planner=lambda: get_agent_graph_state(state=state, state_key="planner_latest"),
#             # selector=lambda: get_agent_graph_state(state=state, state_key="selector_latest"),
#             # reporter=lambda: get_agent_graph_state(state=state, state_key="reporter_latest"),
#             # planner_agent=planner_prompt_template,
#             # selector_agent=selector_prompt_template,
#             # reporter_agent=reporter_prompt_template,
#             # serp=lambda: get_agent_graph_state(state=state, state_key="serper_latest"),
#             prompt=cartagent_prompt_template
#         )
#     )

#     # Creat graph for tools too
#     # graph.add_node(
#     #     "serper_tool",
#     #     lambda state: get_google_serper(
#     #         state=state,
#     #         plan=lambda: get_agent_graph_state(state=state, state_key="planner_latest")
#     #     )
#     # )

#     # graph.add_node(
#     #     "scraper_tool",
#     #     lambda state: scrape_website(
#     #         state=state,
#     #         research=lambda: get_agent_graph_state(state=state, state_key="selector_latest")
#     #     )
#     # )

#     graph.add_node(
#         "posagent", 
#         lambda state: POSAgent(
#             state=state,
#             model=model,
#             server=server,
#             guided_json=pos_guided_json,
#             stop=stop,
#             model_endpoint=model_endpoint,
#             temperature=temperature
#         ).invoke(
#             payment=lambda: get_agent_graph_state(state=state, state_key="reviewer_all"),
#             # planner=lambda: get_agent_graph_state(state=state, state_key="planner_latest"),
#             # selector=lambda: get_agent_graph_state(state=state, state_key="selector_latest"),
#             # reporter=lambda: get_agent_graph_state(state=state, state_key="reporter_latest"),
#             # planner_agent=planner_prompt_template,
#             # selector_agent=selector_prompt_template,
#             # reporter_agent=reporter_prompt_template,
#             # serp=lambda: get_agent_graph_state(state=state, state_key="serper_latest"),
#             prompt=posagent_prompt_template
#         )
#     )

#     graph.add_node(
#         "invoiceemailer", 
#         lambda state: InvoiceEmailAgent(
#             state=state,
#             model=model,
#             server=server,
#             guided_json=invoiceemailer_guided_json,
#             stop=stop,
#             model_endpoint=model_endpoint,
#             temperature=temperature
#         ).invoke(
#             feedback=lambda: get_agent_graph_state(state=state, state_key="reviewer_all"),
#             email=lambda: get_agent_graph_state(state=state, state_key="planner_latest"),
#             # selector=lambda: get_agent_graph_state(state=state, state_key="selector_latest"),
#             # reporter=lambda: get_agent_graph_state(state=state, state_key="reporter_latest"),
#             # planner_agent=planner_prompt_template,
#             # selector_agent=selector_prompt_template,
#             # reporter_agent=reporter_prompt_template,
#             # serp=lambda: get_agent_graph_state(state=state, state_key="serper_latest"),
#             prompt=invoiceemailer_prompt_template
#         )
#     )

#     graph.add_node("end", lambda state: EndNodeAgent(state).invoke())

#     # Define the conditional edges in the agent graph
#     # def pass_review(state: AgentGraphState):
#     #     review_list = state["router_response"]
#     #     if review_list:
#     #         review = review_list[-1]
#     #     else:
#     #         review = "No review"

#     #     if review != "No review":
#     #         if isinstance(review, HumanMessage):
#     #             review_content = review.content
#     #         else:
#     #             review_content = review
            
#     #         review_data = json.loads(review_content)
#     #         next_agent = review_data["next_agent"]
#     #     else:
#     #         next_agent = "end"

#     #     return next_agent

#     # Add edges to the graph
#     graph.set_entry_point("manager")
#     graph.set_finish_point("end")
#     graph.add_edge("manager", "salesagent")
#     graph.add_edge("manager", "customerserviceagent")
#     graph.add_edge("manager", "itemsrecommender")
#     graph.add_edge("manager", "cartagent")
#     graph.add_edge("manager", "posagent")
#     graph.add_edge("manager", "invoiceemailer")

#     # Add coonditional edges too
#     # graph.add_conditional_edges(
#     #     "router",
#     #     lambda state: pass_review(state=state),
#     # )

#     graph.add_edge("invoiceemailer", "end")

#     return graph

# def compile_workflow(graph):
#     workflow = graph.compile()
#     return workflow

# agent_graph/graph.py
import json
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph
from agents.agents import (
    ManagerAgent,
    SalesAgent,
    CustomerServiceAgent,
    ItemsRecommendationAgent,
    CartAgent,
    POSAgent,
    InvoiceEmailAgent,
    EndNodeAgent
)
from prompts.prompts import (
    manager_prompt_template,
    salesagent_prompt_template, 
    customerserviceagent_prompt_template, 
    itemsrecommendationagent_prompt_template, 
    cartagent_prompt_template,
    posagent_prompt_template,
    invoiceemailer_prompt_template,
    manager_guided_json,
    salesagent_guided_json,
    customerserviceagent_guided_json,
    itemsrecommendationagent_guided_json,
    cartagent_guided_json,
    pos_guided_json,
    invoiceemailer_guided_json
)
from states.states import AgentGraphState, get_agent_graph_state, state

def create_graph(server=None, model=None, stop=None, model_endpoint=None, temperature=0):
    graph = StateGraph(AgentGraphState)

    # Manager: determines whether the query is a product inquiry or a complaint
    graph.add_node(
        "manager", 
        lambda state: ManagerAgent(
            state=state,
            model=model,
            server=server,
            guided_json=manager_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            customer_query=state.get("customer_query", ""),
            complaint_query=state.get("customer_complaint", ""),
            prompt=manager_prompt_template
        )
    )

    # Sales Agent for product inquiries
    graph.add_node(
        "salesagent",
        lambda state: SalesAgent(
            state=state,
            model=model,
            server=server,
            guided_json=salesagent_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            customer_query=state.get("customer_query", ""),
            prompt=salesagent_prompt_template,
            feedback=lambda: get_agent_graph_state(state=state, state_key="manager_response")
        )
    )

    # Customer Service Agent for complaints
    graph.add_node(
        "customerserviceagent", 
        lambda state: CustomerServiceAgent(
            state=state,
            model=model,
            server=server,
            guided_json=customerserviceagent_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            customer_complaint=state.get("customer_complaint", ""),
            prompt=customerserviceagent_prompt_template,
            feedback=lambda: get_agent_graph_state(state=state, state_key="manager_response")
        )
    )

    # Items Recommendation Agent (active in parallel)
    graph.add_node(
        "itemsrecommender", 
        lambda state: ItemsRecommendationAgent(
            state=state,
            model=model,
            server=server,
            guided_json=itemsrecommendationagent_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            customer_query=state.get("customer_query", ""),
            prompt=itemsrecommendationagent_prompt_template,
            feedback=lambda: get_agent_graph_state(state=state, state_key="sales_agent_response")
        )
    )

    # Cart Agent for adding items to the cart
    graph.add_node(
        "cartagent", 
        lambda state: CartAgent(
            state=state,
            model=model,
            server=server,
            guided_json=cartagent_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            customer_query=state.get("customer_query", ""),
            prompt=cartagent_prompt_template,
            feedback=lambda: get_agent_graph_state(state=state, state_key="sales_agent_response")
        )
    )

    # POS Agent for payment processing
    graph.add_node(
        "posagent", 
        lambda state: POSAgent(
            state=state,
            model=model,
            server=server,
            guided_json=pos_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            prompt=posagent_prompt_template,
            payment_info=lambda: state.get("cart_total", "0")
        )
    )

    # Invoice Email Agent for sending invoice receipts
    graph.add_node(
        "invoiceemailer", 
        lambda state: InvoiceEmailAgent(
            state=state,
            model=model,
            server=server,
            guided_json=invoiceemailer_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            prompt=invoiceemailer_prompt_template,
            payment_status=lambda: state.get("payment_status", ""),
            email_address=lambda: state.get("customer_email", "customer@example.com")
        )
    )

    # End node
    graph.add_node("end", lambda state: EndNodeAgent(state).invoke())

    # Set entry and finish points
    graph.set_entry_point("manager")
    graph.set_finish_point("end")

    # Edge routing:
    # Manager → SalesAgent OR CustomerServiceAgent (based on a state flag “route” set by the manager)
    graph.add_edge("manager", "salesagent")
    graph.add_edge("manager", "customerserviceagent")

    # SalesAgent decision: if “add_to_cart” flag is set, go to cart; otherwise (or after recommendation) continue exploring.
    def sales_agent_decision(state):
        return "cartagent" if state.get("add_to_cart", False) else "itemsrecommender"
    graph.add_conditional_edges("salesagent", sales_agent_decision)

    # From recommendations, allow a loop to add to cart or keep exploring.
    def recommendation_decision(state):
        return "cartagent" if state.get("add_to_cart", False) else "salesagent"
    graph.add_conditional_edges("itemsrecommender", recommendation_decision)

    # From cart: if the user opts for checkout, proceed to POS; otherwise return to product inquiry.
    def cart_agent_decision(state):
        return "posagent" if state.get("checkout", False) else "salesagent"
    graph.add_conditional_edges("cartagent", cart_agent_decision)

    # After payment: if successful, send invoice; if not, return to cart.
    def pos_agent_decision(state):
        return "invoiceemailer" if state.get("payment_status", "") == "success" else "cartagent"
    graph.add_conditional_edges("posagent", pos_agent_decision)

    # Invoice email → End
    graph.add_edge("invoiceemailer", "end")

    return graph

def compile_workflow(graph):
    workflow = graph.compile()
    return workflow