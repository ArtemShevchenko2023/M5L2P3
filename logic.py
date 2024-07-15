import sqlite3
from config import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


class DB_Map():
    def __init__(self, database):
        self.database = database
    
    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()

    def add_city(self,user_id, city_name ):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]  
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

            
    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))

            cities = [row[0] for row in cursor.fetchall()]
            return cities


    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    def create_grap(self, path, cities, color):
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.stock_img()
        for city in cities:
            lat, lon = self.get_coordinates(city)
            plt.plot([lon], [lat],
            color=f'{color}', linewidth=1, marker='o',
            transform=ccrs.Geodetic(),
            )
            plt.text(lon - 3, lat - 12, city,
            horizontalalignment='right',
            transform=ccrs.Geodetic())
            plt.savefig(path)
    def create_grapf(self, path, city_names, marker_color='blue'):
        fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
        ax.add_feature(cfeature.LAND, color='lightgreen')
        ax.add_feature(cfeature.OCEAN, color='aqua')
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')

        for city in city_names:
            lat, lon = self.get_coordinates(city)  # Функция для получения координат города
            ax.plot(lon, lat, marker='o', color=marker_color, markersize=5, transform=ccrs.Geodetic())
            plt.savefig(path)
    def get_cities_by_country(self, country_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            query = "SELECT city FROM cities WHERE country = ?"
            cursor.execute(query, (country_name,))
            return [row[0] for row in cursor.fetchall()]

    def get_cities_by_density(self, min_density, max_density):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            query = "SELECT city FROM cities WHERE population_density BETWEEN ? AND ?"
            cursor.execute(query, (min_density, max_density))
            return [row[0] for row in cursor.fetchall()]

    def get_cities_by_density_and_country(self, country_name, min_density, max_density):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            query = "SELECT city FROM cities WHERE country = ? AND population_density BETWEEN ? AND ?"
            cursor.execute(query, (country_name, min_density, max_density))
            return [row[0] for row in cursor.fetchall()]


if __name__=="__main__":
    
    m = DB_Map(DATABASE)
    m.create_grapf('image/world.png', ['Saratov', 'Paris', 'New York', 'Satana', 'Samara', 'Moscow', 'London'])
