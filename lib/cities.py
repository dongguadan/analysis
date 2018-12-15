# -*- coding: utf-8 -*-
import json

def get_cities_json():
	cities_json = json.loads("{}")
	identifies_json = json.loads("{}")
	with open('lib/onlyCity.json', 'r', encoding='utf-8') as f:
		cities = f.read()
		cities = cities.replace('\n', '')
		cities = cities.replace(' ', '')
		cities_json = json.loads(cities)

	print(cities_json)
	for city in cities_json["cities"]:
		identify = int(city["code"])
		identifies_json[identify] = city["name"]
	print("{}\n".format(identifies_json))
	return identifies_json