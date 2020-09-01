from rest_framework import viewsets

from django.db.models import Prefetch

from places.models import (
    Places,
    PlaceDetails,
)
from places.serializers import (
    PlacesSerializer,
)


class PlacesSerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = PlacesSerializer

    queryset = Places.objects.all().order_by('-user_ratings_total').prefetch_related(
        Prefetch('placedetails_set',
                 queryset=PlaceDetails.objects.all(),
                 to_attr='place_details'))

    print('queryset', queryset[0].__dict__)
    # queryset_detail = queryset.prefetch_related(
    #     Prefetch('placedetails_set',
    #              queryset=PlaceDetails.objects.all(),
    #              to_attr='place_details')
    # )
    # print('queryset_detail', queryset_detail)
