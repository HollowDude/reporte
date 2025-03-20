''''
from rest_framework import routers
from django.urls import include, path
from app.api.viewsets import clienteViewSet

router = routers.DefaultRouter()

router.register('Cliente', clienteViewSet.Cliente)

urlpatterns = [
    path('', include(router.urls)),
]
'''