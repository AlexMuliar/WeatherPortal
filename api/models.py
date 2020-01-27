from django.db import models

from .apps import ApiConfig
import sqlite3

# Create your models here.

# ** Make raw SQL queries.


class Weather(object):
    __columns__ = ['id', 'city', 'sky', 'temp', 'wind_speed', 'wind_degree', 'clouds', 'time']
    __db_name__ = ApiConfig.db_name
    
    def __init__(self):
        with sqlite3.connect(self.__db_name__) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS weather
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT NOT NULL,
                    sky TEXT, temp FLOAT, wind_speed FLOAT, wind_degree FLOAT,
                    clouds INTEGER, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")


    @staticmethod
    def get_all():
        with sqlite3.connect(Weather.__db_name__) as conn:
            cursor = conn.cursor()
            data = cursor.execute("""
                SELECT * FROM weather
            """).fetchall()

        return [dict(zip(Weather.__columns__, item)) for item in data]

    
    @staticmethod
    def insert(raw):
        query = """INSERT INTO weather
        (city, sky, temp, wind_speed, wind_degree, clouds)
        VALUES ('%s', '%s', %f, %f, %f, %i)
        """
        with sqlite3.connect(Weather.__db_name__) as conn:
            cursor = conn.cursor()
            cursor.execute(query % (
                raw['city'], raw['sky'], raw['temp'], raw['wind_speed'], raw['wind_degree'], raw['clouds']))
            conn.commit()

        return cursor.lastrowid    
        

    @staticmethod    
    def get_by_id(record_id):
        with sqlite3.connect(Weather.__db_name__) as conn:
            cursor = conn.cursor()
            data = cursor.execute(f"""
                SELECT * FROM weather
                WHERE id = { record_id }
            """).fetchone()
        
        return dict(zip(Weather.__columns__, data))


    @staticmethod    
    def get_by_city(city_name):
        with sqlite3.connect(Weather.__db_name__) as conn:
            cursor = conn.cursor()
            data = cursor.execute(f"""
                SELECT * FROM weather
                WHERE city = { city_name }
            """).fetchall()

        return [dict(zip(Weather.__columns__, item)) for item in data]


    @staticmethod    
    def custom_selector(city=None, date_from=None, date_to=None, **kwargs):
        query = "SELECT * FROM weather "
        is_constrain = False

        if city:
            query += f'WHERE city LIKE "{ city }%" '
            is_constrain = True
        if date_from:
            if is_constrain:
                query += 'AND '
            else:
                is_constrain = True
                query += 'WHERE '
            query += f'time >= "{ date_from }" '
        if date_to:
            if is_constrain:
                query += 'AND '
            else:
                query += 'WHERE '
            query += f'time <= "{ date_to }" '
        query += "ORDER BY time DESC;"
        with sqlite3.connect(Weather.__db_name__) as conn:
            cursor = conn.cursor()
            data = cursor.execute(query).fetchall()

        return [dict(zip(Weather.__columns__, item)) for item in data]

    
    @staticmethod    
    def del_by_id(record_id):
        with sqlite3.connect(Weather.__db_name__) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                DELETE FROM weather
                WHERE id = { record_id }
            """)
            conn.commit()
            return cursor.lastrowid



