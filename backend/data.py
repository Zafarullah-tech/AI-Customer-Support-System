# Synthetic FAQ Data for E-commerce Platform

FAQ_DATA = [
    {
        "intent": "order_status",
        "question": "Where is my order?",
        "answer": "You can track your order by visiting the 'My Orders' section in your account profile. If you have the tracking number, you can also track it on our shipping partner's website."
    },
    {
        "intent": "refund_policy",
        "question": "What is your refund policy?",
        "answer": "We offer a 30-day return policy for most items. Items must be in their original condition. Once received, refunds are processed within 5-7 business days."
    },
    {
        "intent": "delivery_time",
        "question": "How long does shipping take?",
        "answer": "Standard shipping typically takes 3-5 business days. Express shipping takes 1-2 business days. International shipping varies by location."
    },
    {
        "intent": "payment_methods",
        "question": "What payment methods do you accept?",
        "answer": "We accept all major credit cards (Visa, MasterCard, Amex), PayPal, and Apple Pay."
    }
]

SYSTEM_PROMPT = """
You are an AI Customer Support Assistant for an E-commerce platform. 
Use the following FAQ data to answer user queries accurately.
If the user's query is not covered by the FAQ, politely inform them and offer to escalate to a human agent.

FAQ Context:
{faq_context}

Guidelines:
- Be polite and professional.
- If you don't know the answer, say you need to escalate.
- Keep responses concise (under 3 sentences).
"""
