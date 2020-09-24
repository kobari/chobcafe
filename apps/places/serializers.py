from rest_framework import serializers

from places.models import (
    Places,
    PlaceDetails,
)


class PlaceDetailsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        # prefechで取得してる為配列になっている
        if instance:
            image_path = f'http://localhost/images/{instance[0].place_id}'
            return {
                # vue-image-lightbox ように変換
                "photos": [
                    {
                        'src': f"{image_path}/{x['photo_reference']}.png",
                        'thumb': f"{image_path}/{x['photo_reference']}.png",
                     } for x in instance[0].photos
                ]
                ,
                'website': instance[0].website,
                'url': instance[0].url,
                'place_id': instance[0].place_id,
            }
        else:
            return {
                "photos": []
            }

    class Meta:
        model = PlaceDetails
        fields = ['website', 'url', 'photos', 'place_id']


class PlacesSerializer(serializers.ModelSerializer):
    place_details = PlaceDetailsSerializer(many=False)

    class Meta:
        model = Places
        fields = '__all__'



