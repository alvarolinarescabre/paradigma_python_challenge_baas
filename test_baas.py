import unittest
import os
import json
from resources import create_app, baas

class BaaSTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name = "testing")
        self.client = self.app.test_client
        self.place_create = json.loads('{"name":"Borabora"}')
        self.place_update = json.loads('{"name":"Mesopotamia"}')

    def returnId(self, action):
        res = self.client().get('/v1/places', content_type='application/json')
        self.assertEqual(res.status_code, 200)        
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        
        for i in result_in_json:
            if i['name'] == action:
                id_test = i['id']

        return id_test

    def test_step_1_baas_creation(self):
        res = self.client().post('/v1/places', data=json.dumps(self.place_create), content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def test_step_2_baas_get_all(self):
        res = self.client().get('/v1/places', content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_step_3_baas_by_id(self):
        id_test = self.returnId(self.place_create['name'])
        
        res = self.client().get(
            '/v1/places/{}'.format(id_test))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Borabora', str(res.data))

    def test_step_4_baas_edited(self):
        id_test = self.returnId(self.place_create['name'])

        res = self.client().put('/v1/places/{}'.format(id_test),
            data=json.dumps(self.place_update),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        
        res = self.client().get('/v1/places/{}'.format(id_test),
                                content_type='application/json')
        self.assertIn(self.place_update['name'], str(res.data))

    def test_step_5_Paas_deletion(self):
        id_test = self.returnId(self.place_update['name'])
        
        res = self.client().delete(
            '/v1/places/{}'.format(id_test))
        self.assertEqual(res.status_code, 201)
