import json
import random

from locust import HttpLocust, TaskSet, task


headers = {'Content-Type': 'application/json'}


class UserBehavior(TaskSet):

    @property
    def auth(self):
        return ('root', 'demo')

    @task(1)
    def create(self):
        data = json.dumps({
            'title': 'test',
            'code': 'test'
        })
        self.client.post(
            '/snippets/', auth=self.auth, data=data, headers=headers)

    @task(20)  # weight
    def list(self):
        self.client.get('/snippets/', auth=self.auth, headers=headers)

    @task(10)
    def retrieve(self):
        id = random.randint(1, 10)
        self.client.get('/snippets/%s/' % id, auth=self.auth, headers=headers)


class WebsiteUser(HttpLocust):
    host = 'http://localhost:9898'
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 10000
