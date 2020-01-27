
import json

def transform_data_to_my_format(raw_data):
    transformed_data = dict()
    transformed_data['city'] = raw_data['name']
    transformed_data['sky'] = raw_data['weather'][0]['main']
    transformed_data['temp'] = raw_data['main']['temp'] - 273.15
    if 'speed' in raw_data['wind']:
        transformed_data['wind_speed'] = raw_data['wind']['speed']
    else:
        transformed_data['wind_speed'] = 0
    if 'deg' in raw_data['wind']:
        transformed_data['wind_degree'] = raw_data['wind']['deg']
    else:
        transformed_data['wind_degree'] = 0
    transformed_data['clouds'] = raw_data['clouds']['all']
    

    return transformed_data


class CityStorage:
    def __init__(self):
        df = json.loads(open('db/cities.json').read())
        l_arr = 'qwertyuiopasdfghjklzxcvbnm'
        groups = dict()
        for l in l_arr:
            groups[l] = list()
            for k in l_arr:
                groups[l+k] = list()
                
        for item in df:
            if item['name'] and item['name'][0].lower() in l_arr:
                groups[item['name'][0].lower()].append(item)
            if item['name'] and item['name'][0].lower() in l_arr and len(item['name']) > 1 and item['name'][1].lower() in l_arr:
                groups[item['name'][0:2].lower()].append(item)
            
        self.cities = groups

    
    def get_cities_on_char(self, c):
        return self.cities[c[:2]]