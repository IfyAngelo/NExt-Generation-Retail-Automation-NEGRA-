# # import json
# # import yaml
# # import os
# from termcolor import colored
# from models.openai_models import get_open_ai, get_open_ai_json
# # from models.ollama_models import OllamaModel, OllamaJSONModel
# # from models.vllm_models import VllmJSONModel, VllmModel
# from models.groq_models import GroqModel, GroqJSONModel
# # from models.claude_models import ClaudModel, ClaudJSONModel
# # from models.gemini_models import GeminiModel, GeminiJSONModel
# from prompts.prompts import (
#     manager_prompt_template,
#     salesagent_prompt_template, 
#     customerserviceagent_prompt_template, 
#     itemsrecommendationagent_prompt_template, 
#     cartagent_prompt_template,
#     invoiceemailer_prompt_template,
# )
# from utils.helper_functions import get_current_utc_datetime, check_for_content
# from states.state import AgentGraphState

# class Agent:
#     def __init__(self, state: AgentGraphState, model=None, server=None, temperature=0, model_endpoint=None, stop=None, guided_json=None):
#         self.state = state
#         self.model = model
#         self.server = server
#         self.temperature = temperature
#         self.model_endpoint = model_endpoint
#         self.stop = stop
#         self.guided_json = guided_json

#     def get_llm(self, json_model=True):
#         if self.server == 'openai':
#             return get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(model=self.model, temperature=self.temperature)
        
#         if self.server == 'groq':
#             return GroqJSONModel(
#                 model=self.model,
#                 temperature=self.temperature
#             ) if json_model else GroqModel(
#                 model=self.model,
#                 temperature=self.temperature
#             )    

#     def update_state(self, key, value):
#         self.state = {**self.state, key: value}

# class ManagerAgent(Agent):
#     def invoke(self, customer_query, prompt=manager_prompt_template, feedback=None):
#         feedback_value = feedback() if callable(feedback) else feedback
#         feedback_value = check_for_content(feedback_value)

#         manager_prompt = prompt.format(
#             feedback=feedback_value,
#             datetime=get_current_utc_datetime()
#         )

#         messages = [
#             {"role": "system", "content": manager_prompt},
#             {"role": "user", "content": f"customer query: {customer_query}"}
#         ]

#         llm = self.get_llm()
#         ai_msg = llm.invoke(messages)
#         response = ai_msg.content

#         self.update_state("manager_response", response)
#         print(colored(f"Manager 👩🏿‍💻: {response}", 'cyan'))
#         return self.state

# class SalesAgent(Agent):
#     def invoke(self, customer_query, prompt=salesagent_prompt_template, feedback=None, previous_query=None): #,serp=None):
#         feedback_value = feedback() if callable(feedback) else feedback
#         previous_queried_item = previous_query() if callable(previous_query) else previous_query

#         feedback_value = check_for_content(feedback_value)
#         previous_queried_item = check_for_content(previous_queried_item)

#         salesagent_prompt = prompt.format(
#             feedback=feedback_value,
#             previous_selections=previous_queried_item,
#             # serp=serp().content,
#             datetime=get_current_utc_datetime()
#         )

#         messages = [
#             {"role": "system", "content": salesagent_prompt},
#             {"role": "user", "content": f"customer_query: {customer_query}"}
#         ]

#         llm = self.get_llm()
#         ai_msg = llm.invoke(messages)
#         response = ai_msg.content

#         print(colored(f"Sales Agent 🧑🏼‍💻: {response}", 'green'))
#         self.update_state("sales_agent_response", response)
#         return self.state

# class CustomerServiceAgent(Agent):
#     def invoke(self, customer_complaint, prompt=customerserviceagent_prompt_template, feedback=None, previous_complaint=None, research=None):
#         feedback_value = feedback() if callable(feedback) else feedback
#         previous_complaint_value = previous_complaint() if callable(previous_complaint) else previous_complaint
#         research_value = research() if callable(research) else research

#         feedback_value = check_for_content(feedback_value)
#         previous_complaint_value = check_for_content(previous_complaint_value)
#         research_value = check_for_content(research_value)
        
#         customerserviceagent_prompt = prompt.format(
#             feedback=feedback_value,
#             previous_reports=previous_complaint_value,
#             datetime=get_current_utc_datetime(),
#             research=research_value
#         )

#         messages = [
#             {"role": "system", "content": customerserviceagent_prompt},
#             {"role": "user", "content": f"customer question: {customer_complaint}"}
#         ]

#         llm = self.get_llm(json_model=False)
#         ai_msg = llm.invoke(messages)
#         response = ai_msg.content

#         print(colored(f"Customer Service Agent 👨‍💻: {response}", 'yellow'))
#         self.update_state("customer_service_agent_response", response)
#         return self.state

# class ItemsRecommendationAgent(Agent):
#     def invoke(self, customer_query, prompt=itemsrecommendationagent_prompt_template, recommender=None, feedback=None):
#         recommender_value = recommender() if callable(recommender) else recommender
#         feedback_value = feedback() if callable(feedback) else feedback

#         recommender_value = check_for_content(recommender_value)
#         feedback_value = check_for_content(feedback_value)
        
#         recommendationagent_prompt = prompt.format(
#             reporter=recommender_value,
#             state=self.state,
#             feedback=feedback_value,
#             datetime=get_current_utc_datetime(),
#         )

#         messages = [
#             {"role": "system", "content": recommendationagent_prompt},
#             {"role": "user", "content": f"customer query: {customer_query}"}
#         ]

#         llm = self.get_llm()
#         ai_msg = llm.invoke(messages)
#         response = ai_msg.content

#         print(colored(f"Recommendation Agent 👩🏽‍⚖️: {response}", 'magenta'))
#         self.update_state("items_recommendation_agent_response", response)
#         return self.state
    
# class CartAgent(Agent):
#     def invoke(self, customer_query, feedback=None, prompt=cartagent_prompt_template):
#         feedback_value = feedback() if callable(feedback) else feedback
#         feedback_value = check_for_content(feedback_value)

#         cartagent_prompt = prompt.format(feedback=feedback_value)

#         messages = [
#             {"role": "system", "content": cartagent_prompt},
#             {"role": "user", "content": f"research question: {customer_query}"}
#         ]

#         llm = self.get_llm()
#         ai_msg = llm.invoke(messages)
#         response = ai_msg.content

#         print(colored(f"Cart Items Agent 🧭: {response}", 'blue'))
#         self.update_state("cart_agent_response", response)
#         return self.state

# class POSAgent(Agent):
#     def invoke(self, payment=None):
#         payment_value = payment() if callable(payment) else payment
#         response = payment_value.content

#         print(colored(f"POS Report 📝: {response}", 'blue'))
#         self.update_state("pos_agent_response", response)
#         return self.state
    
# class InvoiceEmailAgent(Agent):
#     def invoke(self, feedback=None, email=None, prompt=invoiceemailer_prompt_template):
#         feedback_value = feedback() if callable(feedback) else feedback
#         email_value = email() if callable(email) else email

#         invoiceemailagent_prompt = prompt.format(
#             feedback=feedback_value,
#             email=email_value,
#             state=self.state,
#             datetime=get_current_utc_datetime
#         )

#         messages = [
#             {"role": "system", "content": invoiceemailagent_prompt},
#             {"role": "user", "content": f"email: {email}"}
#         ]

#         llm = self.get_llm()
#         ai_msg = llm.invoke(messages)
#         response = ai_msg.content

#         print(colored(f"Invoice Email Agent 👩🏽‍⚖️: {response}", 'cyan'))
#         self.update_state("invoice_email_agent", response)
#         return self.state

# class EndNodeAgent(Agent):
#     def invoke(self):
#         self.update_state("end_chain", "end_chain")
#         return self.state

# agents/agents.py
from termcolor import colored
from models.openai_models import get_open_ai, get_open_ai_json
from prompts.prompts import (
    manager_prompt_template,
    salesagent_prompt_template, 
    customerserviceagent_prompt_template, 
    itemsrecommendationagent_prompt_template, 
    cartagent_prompt_template,
    posagent_prompt_template,
    invoiceemailer_prompt_template,
)
from utils.helper_functions import get_current_utc_datetime, check_for_content
from states.states import AgentGraphState

# Import custom tools
from tools.product_retrieval import retrieve_product_info
from tools.complaint_retrieval import retrieve_complaint_info
from tools.payment_gateway import process_payment
from tools.email_service import send_invoice_email

class Agent:
    def __init__(self, state: AgentGraphState, model=None, server=None, temperature=0, model_endpoint=None, stop=None, guided_json=None):
        self.state = state
        self.model = model
        self.server = server
        self.temperature = temperature
        self.model_endpoint = model_endpoint
        self.stop = stop
        self.guided_json = guided_json

    def get_llm(self, json_model=True):
        if self.server == 'openai':
            return get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(model=self.model, temperature=self.temperature)
        # Default to OpenAI if no server specified
        return get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(model=self.model, temperature=self.temperature)

    def update_state(self, key, value):
        self.state[key] = value

class ManagerAgent(Agent):
    def invoke(self, customer_query, complaint_query, prompt=manager_prompt_template, feedback=None):
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)
        
        manager_prompt = prompt.format(
            feedback=feedback_value,
            datetime=get_current_utc_datetime()
        )
        
        # Route decision: if a complaint is provided, set route to "complaint"; else default to "sales"
        route = "complaint" if complaint_query and complaint_query.strip() else "sales"
        self.update_state("route", route)
        
        messages = [
            {"role": "system", "content": manager_prompt},
            {"role": "user", "content": f"Customer Query: {customer_query}\nComplaint: {complaint_query}"}
        ]
        
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        
        self.update_state("manager_response", response)
        print(colored(f"Manager 👩🏿‍💻: {response}", 'cyan'))
        return self.state

class SalesAgent(Agent):
    def invoke(self, customer_query, prompt=salesagent_prompt_template, feedback=None):
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)
        
        # Retrieve product information via a custom RAG tool
        product_info = retrieve_product_info(customer_query)
        self.update_state("product_info", product_info)
        
        salesagent_prompt = prompt.format(
            feedback=feedback_value,
            product_info=product_info,
            datetime=get_current_utc_datetime()
        )
        
        messages = [
            {"role": "system", "content": salesagent_prompt},
            {"role": "user", "content": f"Customer Query: {customer_query}"}
        ]
        
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        
        print(colored(f"Sales Agent 🧑🏼‍💻: {response}", 'green'))
        self.update_state("sales_agent_response", response)
        
        # Simulate decision: if the response contains “add to cart” then set flag
        self.update_state("add_to_cart", "add to cart" in response.lower())
        
        return self.state

class CustomerServiceAgent(Agent):
    def invoke(self, customer_complaint, prompt=customerserviceagent_prompt_template, feedback=None):
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)
        
        # Retrieve complaint resolution info via a custom RAG tool
        complaint_info = retrieve_complaint_info(customer_complaint)
        self.update_state("complaint_info", complaint_info)
        
        customerserviceagent_prompt = prompt.format(
            feedback=feedback_value,
            complaint_info=complaint_info,
            datetime=get_current_utc_datetime()
        )
        
        messages = [
            {"role": "system", "content": customerserviceagent_prompt},
            {"role": "user", "content": f"Customer Complaint: {customer_complaint}"}
        ]
        
        llm = self.get_llm(json_model=False)
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        
        print(colored(f"Customer Service Agent 👨‍💻: {response}", 'yellow'))
        self.update_state("customer_service_agent_response", response)
        return self.state

class ItemsRecommendationAgent(Agent):
    def invoke(self, customer_query, prompt=itemsrecommendationagent_prompt_template, feedback=None):
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)
        
        # Generate a simulated recommendation based on the query
        recommendation = f"Recommended Product for '{customer_query}' (simulated)"
        self.update_state("recommendation", recommendation)
        
        recommendationagent_prompt = prompt.format(
            recommendation=recommendation,
            feedback=feedback_value,
            datetime=get_current_utc_datetime()
        )
        
        messages = [
            {"role": "system", "content": recommendationagent_prompt},
            {"role": "user", "content": f"Customer Query: {customer_query}"}
        ]
        
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        
        print(colored(f"Recommendation Agent 👩🏽‍⚖️: {response}", 'magenta'))
        self.update_state("items_recommendation_agent_response", response)
        return self.state

class CartAgent(Agent):
    def invoke(self, customer_query, prompt=cartagent_prompt_template, feedback=None):
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)
        
        # Simulate adding product to cart using the retrieved product_info
        product_info = self.state.get("product_info", "No product info")
        cart_items = self.state.get("cart_items", [])
        cart_items.append(product_info)
        self.update_state("cart_items", cart_items)
        
        # Update the cart total (for simulation, assume each product costs $10)
        cart_total = self.state.get("cart_total", 0) + 10
        self.update_state("cart_total", cart_total)
        
        cartagent_prompt = prompt.format(
            feedback=feedback_value,
            product_info=product_info,
            cart_total=cart_total
        )
        
        messages = [
            {"role": "system", "content": cartagent_prompt},
            {"role": "user", "content": f"Adding product to cart: {product_info}"}
        ]
        
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        
        print(colored(f"Cart Agent 🧭: {response}", 'blue'))
        self.update_state("cart_agent_response", response)
        
        # Simulate checkout decision: if “checkout” appears in the response, flag checkout
        self.update_state("checkout", "checkout" in response.lower())
        
        return self.state

class POSAgent(Agent):
    def invoke(self, prompt=posagent_prompt_template, payment_info=None):
        # Simulate payment processing via a custom payment gateway tool
        payment_response = process_payment(payment_info)
        self.update_state("payment_status", payment_response.get("status", "failed"))
        
        posagent_prompt = prompt.format(
            payment_status=payment_response.get("status", "failed"),
            cart_total=self.state.get("cart_total", 0),
            datetime=get_current_utc_datetime()
        )
        
        messages = [
            {"role": "system", "content": posagent_prompt},
            {"role": "user", "content": f"Processing payment for amount: {self.state.get('cart_total', 0)}"}
        ]
        
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        
        print(colored(f"POS Agent 📝: {response}", 'blue'))
        self.update_state("pos_agent_response", response)
        return self.state

class InvoiceEmailAgent(Agent):
    def invoke(self, prompt=invoiceemailer_prompt_template, payment_status=None, email_address=None):
        # Simulate sending an invoice email via a custom email service tool
        email_response = send_invoice_email(email_address, self.state.get("cart_items", []), self.state.get("cart_total", 0))
        self.update_state("invoice_email_status", email_response.get("status", "failed"))
        
        invoiceemailer_prompt = prompt.format(
            payment_status=payment_status,
            email_address=email_address,
            invoice_status=email_response.get("status", "failed"),
            datetime=get_current_utc_datetime()
        )
        
        messages = [
            {"role": "system", "content": invoiceemailer_prompt},
            {"role": "user", "content": f"Sending invoice email to: {email_address}"}
        ]
        
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        
        print(colored(f"Invoice Email Agent 👩🏽‍⚖️: {response}", 'cyan'))
        self.update_state("invoice_email_agent", response)
        return self.state

class EndNodeAgent(Agent):
    def invoke(self):
        self.update_state("end_chain", "end_chain")
        print("End of workflow.")
        return self.state