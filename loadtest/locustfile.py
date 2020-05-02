import random
import json
from locust import HttpLocust, TaskSequence, task, seq_task, between
from locust.exception import StopLocust
from locust.contrib.fasthttp import FastHttpLocust


class MalaMaturaTaskSet(TaskSequence):

    @seq_task(1)
    def get_index(self):
        if hasattr(self, 'token'):
            raise StopLocust()
        self.client.get('/')

    @seq_task(2)
    def login(self):
        r = self.client.post('/api/token-auth/', {'username': 'ucenik.1@gmail.com', 'password': '12345'})
        if r.status_code != 200:
            raise StopLocust()
        self.token = r.json()['token']
        self.headers = {'Authorization': f'JWT {self.token}', 'Content-Type': 'application/json'}

    @seq_task(3)
    def get_testovi(self):
        r = self.client.get('/api/testovi/', headers=self.headers)
        if r.status_code != 200:
            raise StopLocust()
        self.test_id = r.json()[0]['id']

    @seq_task(4)
    def get_test(self):
        self.client.get(f'/api/testovi/{self.test_id}/', headers=self.headers)

    @seq_task(5)
    def get_test_komplet(self):
        r = self.client.get(f'/api/komplet-test/{self.test_id}/', headers=self.headers)
        if r.status_code != 200:
            raise StopLocust()
        self.pitanja = [pitanje['id'] for pitanje in r.json()['pitanje_set']]

    @seq_task(6)
    def zapocni_test(self):
        body = f'{{"test": {self.test_id} }}'.encode('ascii')
        r = self.client.post('/api/pocetak/', body, headers=self.headers)
        if r.status_code != 201:
            raise StopLocust()
        self.test_ucenika_id = r.json()['test_ucenika']
        self.odgovor_count = 0

    @seq_task(7)
    @task(20)
    def posalji_odgovor(self):
        odg = {
            'test_ucenika': self.test_ucenika_id,
            'pitanje': self.pitanja[self.odgovor_count],
            'odgovor': str(random.randrange(1, 5))
        }
        self.odgovor_count += 1
        r = self.client.post('/api/odgovor/', json.dumps(odg).encode('ascii'), headers=self.headers)

    @seq_task(8)
    def get_rezime(self):
        self.client.get(f'/api/rezime/{self.test_ucenika_id}/', headers=self.headers, name='/api/rezime/')

    @seq_task(9)
    def post_zavrsi(self):
        body = json.dumps({'test_ucenika': self.test_ucenika_id}).encode('ascii')
        self.client.post('/api/kraj/', body, headers=self.headers)
        raise StopLocust()


class Ucenik(FastHttpLocust):
    task_set = MalaMaturaTaskSet
    wait_time = between(10, 60)
