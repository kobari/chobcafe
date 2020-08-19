import json
import time
import os

from django.conf import settings
from django.core import serializers
from django.db import transaction

import requests

from places.models import Places as PlacesModel


class Places:
    KEY = 'AIzaSyDSTFj49ERA0vcjk56S-UNs6RYkCkeNAL8'
    PHOTO_URL = 'https://maps.googleapis.com/maps/api/place/photo'
    TEXT_SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

    def text_search(self):
        i=1
        url = f"{self.TEXT_SEARCH_URL}?key={self.KEY}&query=cafe bangkok"
        res = requests.get(url)
        print(res.url)
        json_data = res.json()
        next_page_token = json_data.get('next_page_token')
        print('next_page_token', i, next_page_token)

        if res.status_code >= 400:
            print('status_code error')
            exit
        with open(f'{i}.json', 'wb') as fp:
            fp.write(res.content)

        while next_page_token != None:
            time.sleep(2)
            url = f"{self.TEXT_SEARCH_URL}?key={self.KEY}&pagetoken={next_page_token}"
            res = requests.get(url)
            print(res.url)
            json_data = res.json()
            next_page_token = json_data.get('next_page_token')
            i += 1
            print('next_page_token', i, next_page_token)
            if res.status_code >= 400:
                print('status_code error')
                exit
            with open(f'{i}.json', 'wb') as fp:
                fp.write(res.content)

    def place_photos(self):
        for i in range(1, 4):
            filepath = os.path.join(settings.BASE_DIR,
                                    f'../{i}.json')
            with open(filepath, 'r') as fp:
                data = json.load(fp)
                #print(data)
                for item in data['results']:
                    if 'photos' in item:
                        url = f"{self.PHOTO_URL}?key={self.KEY}&photoreference={item['photos'][0]['photo_reference']}&maxheight={item['photos'][0]['height']}&maxwidth={item['photos'][0]['width']}"
                        res = requests.get(url)
                        image_path = os.path.join(settings.BASE_DIR,
                                                  f"../images/{item['name']}.png")
                        with open(image_path, 'wb') as fp2:
                            fp2.write(res.content)

    def bulk_insert(self):

        with transaction.atomic():
            for i in range(1, 4):
                filepath = os.path.join(settings.BASE_DIR,
                                        f'../{i}.json')
                print(filepath)
                with open(filepath, 'r') as fp:
                    data = json.load(fp)
                    insert_data = []
                    for item in data['results']:
                        print(item['rating'], item['user_ratings_total'])
                        insert_data.append(PlacesModel(
                               place_id=item['place_id'],
                               business_status=item['business_status'],
                               name=item['name'],
                               formatted_address=item['formatted_address'],
                               rating=item['rating'],
                               user_ratings_total=item['user_ratings_total'],
                               photos=item.get('photos'),
                               geometry=item['geometry'],
                               types=item['types'],
                               )
                        )
                    PlacesModel.objects.bulk_create(insert_data)

    def write_json(self):
        models = PlacesModel.objects.order_by('-user_ratings_total')
        json_res = serializers.serialize('json', models)
        json_res = json.loads(json_res)
        #print(type(json_res), json_res)
        filepath = os.path.join(settings.BASE_DIR,
                                '../assets/output.json')
        write_data = []
        for item in json_res:
            tmp = item['fields']
            tmp['place_id'] = item['pk']
            write_data.append(tmp)

        write_data = json.dumps(write_data, indent=4)
        with open(filepath, 'w') as fp:
            fp.writelines(write_data)
