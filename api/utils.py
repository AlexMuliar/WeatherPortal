


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