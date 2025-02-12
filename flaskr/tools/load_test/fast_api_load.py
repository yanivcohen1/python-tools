import random
from locust import HttpUser, task, between

# https://www.youtube.com/watch?v=esIEW0aEKqk

sentences = [
    "That's just what I needed today",
    "I love coding in python",
    "Well what a surprise",
    "James hates eating onions",
]
# host = "http://127.0.0.1:5000"


class AppUser(HttpUser):

    wait_time = between(2, 5)  # wait

    @task
    def index_page(self):
        response = self.client.get("/")
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        assert "Hello FastAPI" in response.text, "Expected content not found in response"

    @task
    def sentiment_page(self):
        mytext = random.choice(sentences)
        self.client.get("/sentiment/" + str(mytext))
