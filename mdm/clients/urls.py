from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mdm.clients import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(
    r'clients/get',
    views.ClienteRetrieveView
)
router.register(r'clients', views.ClientViewSet)
router.register(r'carritos', views.CarritoViewSet)

urlpatterns = [
    path('', include(router.urls))
]
