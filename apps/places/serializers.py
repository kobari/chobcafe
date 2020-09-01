from rest_framework import serializers

from places.models import (
    Places,
    PlaceDetails,
)


class PlaceDetailsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        # prefechで取得してる為配列になっている
        data = super(PlaceDetailsSerializer, self).to_representation(instance[0])
        return data

    class Meta:
        model = PlaceDetails
        fields = ['website', 'url', 'photos']


class PlacesSerializer(serializers.ModelSerializer):
    place_details = PlaceDetailsSerializer(many=False)

    class Meta:
        model = Places
        fields = '__all__'



