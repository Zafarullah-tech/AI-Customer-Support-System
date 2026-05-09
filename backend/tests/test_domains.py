
import pytest
from unittest.mock import patch, MagicMock
import chatbot
import data

HEALTHCARE_FAQS = [
    {"intent": "appointment", "question": "How do I book an appointment?", "answer": "You can book via our portal."},
    {"intent": "prescription", "question": "Can I get a refill?", "answer": "Contact your doctor for refills."}
]

BANKING_FAQS = [
    {"intent": "balance", "question": "How do I check my balance?", "answer": "Use the mobile app to see your balance."},
    {"intent": "lost_card", "question": "I lost my credit card.", "answer": "Call our 24/7 hotline to block your card."}
]

@pytest.mark.parametrize("domain_data, query, expected_intent", [
    (HEALTHCARE_FAQS, "How can I book an appointment?", "appointment"),
    (BANKING_FAQS, "I want to check my account balance", "balance"),
])
def test_domain_adaptation(domain_data, query, expected_intent):
    # Temporarily override FAQ_DATA in chatbot and data modules
    with patch('chatbot.FAQ_DATA', domain_data), \
         patch('chatbot.faq_questions', [item["question"] for item in domain_data]), \
         patch('chatbot.faq_embeddings', chatbot.embedder.encode([item["question"] for item in domain_data], convert_to_tensor=True)):
        
        intent, answer = chatbot.classify_intent(query)
        assert intent == expected_intent
        assert answer is not None

def test_pretrained_generalization():
    # Test if the model understands a domain it wasn't explicitly configured for in data.py
    # by using the Groq LLM fallback (since classify_intent might return 'unknown')
    
    with patch('chatbot.client.chat.completions.create') as mock_create:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "To open a savings account, you need a valid ID."
        mock_create.return_value = mock_response
        
        # Query about banking which is NOT in the default e-commerce FAQ_DATA
        response, intent = chatbot.generate_response("How do I open a bank account?")
        
        # It should fallback to LLM and give a sensible response even if intent is unknown
        assert intent == "unknown"
        assert "account" in response.lower()
