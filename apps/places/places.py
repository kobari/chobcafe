import json
import time
import os
from pathlib import Path
from decimal import Decimal

from django.conf import settings
from django.core import serializers
from django.db import transaction
from django.db.models import Prefetch

import requests

from places.models import (
    Places as PlacesModel,
    PlaceDetails,
)





class Places:
    KEY = 'AIzaSyDSTFj49ERA0vcjk56S-UNs6RYkCkeNAL8'
    PHOTO_URL = 'https://maps.googleapis.com/maps/api/place/photo'
    TEXT_SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    PLACE_DETAIL_URL = 'https://maps.googleapis.com/maps/api/place/details/json'

    def decimal_default_proc(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError

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

    def place_detail(self, place_id=None):
        if place_id:
            print('place_detail place_id=', place_id)
            place_ids = PlacesModel.objects.filter(place_id__in=place_id
                                                   ).values_list('place_id',
                                                                 flat=True).order_by('-user_ratings_total')
        else:
            place_ids = PlacesModel.objects.values_list('place_id', flat=True
                                                        ).order_by('-user_ratings_total')
        for place_id in place_ids:
            url = f"{self.PLACE_DETAIL_URL}?key={self.KEY}&place_id={place_id}"
            res = requests.get(url)
            print(res.url)
            with open(f'./data/{place_id}.json', 'wb') as fp:
                fp.write(res.content)
            time.sleep(2)

    def place_photos(self):
        models = PlaceDetails.objects.exclude(photos=None)
        for model in models:
            dir_path = f'{settings.BASE_DIR}/../front/public/images/{model.place_id}'
            os.makedirs(dir_path, exist_ok=True)
            #data = json.(model.photos)
            #print(type(model.photos), model.photos)
            for i, photo in enumerate(model.photos):
                url = f"{self.PHOTO_URL}?key={self.KEY}&photoreference={photo['photo_reference']}&maxheight={photo['height']}&maxwidth={photo['width']}"
                res = requests.get(url)
                image_path = os.path.join(dir_path,
                                          f"./{photo['photo_reference']}.png")
                with open(image_path, 'wb') as fp2:
                    fp2.write(res.content)
                time.sleep(2)

    def places_bulk_insert(self):

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

    def place_details_bulk_insert(self):
        p = Path(f'{settings.BASE_DIR}/../data')
        with transaction.atomic():
            insert_data = []
            for filepath in p.glob('*.json'):
                print(filepath)
                with open(filepath, 'r') as fp:
                    data = json.load(fp)
                    item = data['result']
                    insert_data.append(PlaceDetails(
                        place=PlacesModel.objects.get(place_id=item['place_id']),
                        url=item.get('url'),
                        website=item.get('website'),
                        photos=item.get('photos'),
                        reviews=item.get('reviews'),
                        opening_hours=item.get('opening_hours'),
                        address_components=item.get('address_components'),
                        )
                    )
            PlaceDetails.objects.bulk_create(insert_data)

    def write_json(self):
        models = PlacesModel.objects.exclude(
            photos=None
        ).order_by(
            '-user_ratings_total'
        ).prefetch_related(Prefetch('placedetails_set',
                                    queryset=PlaceDetails.objects.all(),
                                    to_attr='place_details')
                           )
        filepath = os.path.join(settings.BASE_DIR,
                                '../assets/output.json')
        write_data = []
        for item in models:
            tmp = {
                'place_id': item.place_id,
                'name': item.name,
                'business_status': item.business_status,
                'rating': item.rating,
                'user_ratings_total': item.user_ratings_total,
                'formatted_address': item.formatted_address,
                'photos': item.photos,
                'url': item.place_details[0].url,
                'website': item.place_details[0].website,
            }
            write_data.append(tmp)

        write_data = json.dumps(write_data, indent=4,
                                default=self.decimal_default_proc)
        with open(filepath, 'w') as fp:
            fp.writelines(write_data)
