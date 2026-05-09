
import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chatbot
from data import FAQ_DATA

def test_classify_intent_known():
    # Test with a question very similar to one in FAQ_DATA
    query = "Where is my package?" # Similar to "Where is my order?"
    intent, answer = chatbot.classify_intent(query)
    assert intent == "order_status"
    assert answer is not None

def test_classify_intent_unknown():
    # Test with a question unrelated to the FAQs
    query = "What is the weather today?"
    intent, answer = chatbot.classify_intent(query)
    assert intent == "unknown"
    assert answer is None

@patch('chatbot.client.chat.completions.create')
def test_generate_response_faq(mock_create):
    # Mock Groq response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Your order is on the way."
    mock_create.return_value = mock_response
    
    response, intent = chatbot.generate_response("Where is my order?")
    assert intent == "order_status"
    assert "order" in response.lower()

def test_escalation_logic_trigger():
    # According to requirements: Ensure escalation triggers when confidence < threshold.
    # In our chatbot.py, low confidence returns "unknown" intent.
    query = "I want to speak to a manager"
    intent, _ = chatbot.classify_intent(query)
    assert intent == "unknown"
