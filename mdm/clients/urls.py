from django.urls import include, path

from rest_framework.routers import DefaultRouter

from mdm.clients import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(
    r'clients/get',
    views.ClienteRetrieveView
)
router.register(r'clients', views.ClientViewSet)
router.register(r'carts', views.CarritoViewSet)
router.register(
    r'directions/get',
    views.CodigoPostalRetrieveView
)

urlpatterns = [
    path('', include(router.urls))
]
