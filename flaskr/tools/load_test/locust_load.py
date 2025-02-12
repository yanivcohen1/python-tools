from locust import HttpUser, TaskSet, task, between
import json

class UserBehavior(TaskSet):

    def on_start(self):
        # Login and obtain JWT token
        response = self.client.post("/login", json={"username": "user", "password": "pass"}, cookies={"cookie_name": "cookie_value"}  )
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(1)
    def create_item(self):
        self.client.post("/items", json={"name": "item1", "description": "An item"}, headers=self.headers)

    @task(2)
    def read_item(self):
        self.client.get("/items/1", headers=self.headers)

    @task(3)
    def update_item(self):
        self.client.put("/items/1", json={"name": "item1_updated", "description": "An updated item"}, headers=self.headers)

    @task(4)
    def delete_item(self):
        self.client.delete("/items/1", headers=self.headers)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5) # wait between 1 and 5 seconds after each task
    host = "http://your-api-url.com"  # Replace with your API URL
    min_wait = 1000  # Minimum wait time in milliseconds
    max_wait = 5000  # Maximum wait time in milliseconds

def run_locust():
    import os
    import subprocess

    # Define the number of users and spawn rate
    # in 10 sec all users run (100 users = 10 users/sec * 10 sec)
    num_users = 100 # 100 users
    spawn_rate = 10 # 10 users per second

    # Command to run Locust with specified options
    cmd = [
        "locust",
        "-f", "locustfile.py",
        "--headless",
        "-u", str(num_users),
        "-r", str(spawn_rate),
        "--run-time", "1m",  # Duration of the test
        "--csv", "locust_report",  # Prefix for the CSV report files
        "--host", "http://your-api-url.com"  # Replace with your API URL
    ]

    subprocess.run(cmd)

if __name__ == "__main__":
    run_locust()
