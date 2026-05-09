
from locust import HttpUser, task, between

class ChatbotUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def ask_faq(self):
        self.client.post("/ask", json={"query": "Where is my order?"})

    @task(1)
    def ask_unknown(self):
        self.client.post("/ask", json={"query": "What is the meaning of life?"})

    @task(1)
    def view_logs(self):
        self.client.get("/logs")

    @task(1)
    def escalate(self):
        # First get an ID to escalate (simplified for load test)
        response = self.client.post("/ask", json={"query": "Escalate me"})
        if response.status_code == 200:
            interaction_id = response.json().get("id")
            if interaction_id:
                self.client.post("/escalate", json={"interaction_id": interaction_id})
