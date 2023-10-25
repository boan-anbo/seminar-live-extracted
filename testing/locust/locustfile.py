import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)
    #
    # @task
    # def month_webinar(self):
    #     self.client.get("/webinars/month/")
    #     # self.client.get("/tags")
    #
    # @task
    # def month_webinar_uncached(self):
    #     self.client.get("/webinars/month_uncached/")

    @task
    def detail(self):
        self.client.get("/webinars/short_url/2021-01-28_sample-webiar-252/")

    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)
    #
    # def on_start(self):
    #     # self.client.post("/login", json={"username":"foo", "password":"bar"})
    #     print('Te')