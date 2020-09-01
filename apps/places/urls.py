from django.urls import include, path

from rest_framework import routers

from .views import PlacesSerViewSet

router = routers.DefaultRouter()
router.register(r'list', PlacesSerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
