from django.test import TestCase
from .models import Weather

# Create your tests here.

class WeatherTestCase(TestCase):
    def setUp(self):
        self.example_data = {'city': 'TestCase', 'sky': 'Clouds', 'temp': 279.37, 'wind_speed': 2.47, 'wind_degree': 195.0, 'clouds': 62}


    def test_read_all(self):
        try_read = Weather.get_all()
        self.assertIsInstance(try_read, list)
        self.assertIsInstance(try_read[-1], dict)
        self.assertIsInstance(try_read[-1]['id'], int)


    def test_insert(self):
        db_size = Weather.get_all().__len__()
        try_insert = Weather.insert(self.example_data)
        new_db_size = Weather.get_all().__len__()
        self.assertIsInstance(try_insert, int)
        self.assertEqual(new_db_size, db_size + 1)


    def test_read_one(self):
        last_id = Weather.get_all()[-1]['id']
        try_read = Weather.get_by_id(last_id)
        self.assertIsInstance(try_read, dict)
        self.assertIsInstance(try_read['id'], int)
        self.assertEqual(try_read['city'], self.example_data['city'])
        self.assertEqual(try_read['temp'], self.example_data['temp'])
        
    
    def test_delete(self):
        last_id = Weather.get_all()[-1]['id']
        try_delete = Weather.del_by_id(last_id)
        self.assertEqual(try_delete, 0)

