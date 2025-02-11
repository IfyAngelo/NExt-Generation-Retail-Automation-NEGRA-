# manager_prompt_template = """
# """

# manager_guided_json = {

# }

# # ============================== SALES AGENT ==============================
# saleagent_prompt_template = """
# """

# salesagent_guided_json = {

# }

# # ============================== CUSTOMER SERVICE AGENT ==============================
# customerserviceagent_prompt_template = """
# """

# customerserviceagent_guided_json = {

# }

# # ============================== ITEMS RECOMMENDATION AGENT ==============================
# itemsrecommendationagent_prompt_template = """
# """

# itemsrecommendationagent_guided_json = {

# }

# # ============================== CART AGENT ==============================
# cartagent_prompt_template = """
# """

# cartagent_guided_json = {

# }

# # ============================== INVOICE EMAIL AGENT ==============================
# invoiceemailer_prompt_template = """
# """

# invoiceemailer_guided_json = {

# }

# prompts/prompts.py

# Manager Prompt: instruct the agent to determine routing.
manager_prompt_template = """
[Manager Prompt]
Current Time: {datetime}
Feedback: {feedback}
Please analyze the customer input and determine if this is a product inquiry or a complaint.
"""

manager_guided_json = {
    # (Add any guided parameters if needed)
}

# Sales Agent Prompt: for product inquiries.
salesagent_prompt_template = """
[Sales Agent Prompt]
Current Time: {datetime}
Feedback: {feedback}
Product Information: {product_info}
Please provide detailed product information and ask if the customer would like to add the item to the cart.
"""

salesagent_guided_json = {
}

# Customer Service Agent Prompt: for handling complaints.
customerserviceagent_prompt_template = """
[Customer Service Agent Prompt]
Current Time: {datetime}
Feedback: {feedback}
Complaint Information: {complaint_info}
Please address the customer complaint and provide a resolution.
"""

customerserviceagent_guided_json = {
}

# Items Recommendation Agent Prompt.
itemsrecommendationagent_prompt_template = """
[Items Recommendation Agent Prompt]
Current Time: {datetime}
Feedback: {feedback}
Based on the conversation, please provide a recommendation.
Recommendation: {recommendation}
"""

itemsrecommendationagent_guided_json = {
}

# Cart Agent Prompt.
cartagent_prompt_template = """
[Cart Agent Prompt]
Feedback: {feedback}
Product Information: {product_info}
Current Cart Total: ${cart_total}
Please confirm adding the product to the cart. If the customer wishes to checkout, indicate 'checkout'.
"""

cartagent_guided_json = {
}

# POS Agent Prompt: Payment Processing.
posagent_prompt_template = """
[POS Agent Prompt]
Current Time: {datetime}
Processing payment for amount: ${cart_total}.
Payment Status: {payment_status}
Please confirm whether the payment was successful.
"""

pos_guided_json = {
}

# Invoice Email Agent Prompt.
invoiceemailer_prompt_template = """
[Invoice Email Agent Prompt]
Current Time: {datetime}
Payment Status: {payment_status}
Invoice will be sent to: {email_address}.
Invoice Email Status: {invoice_status}
Please confirm the invoice has been sent.
"""

invoiceemailer_guided_json = {
}
# ============================== END OF PROMPTS ==============================