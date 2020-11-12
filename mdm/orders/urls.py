from django.urls import include, path

from rest_framework.routers import DefaultRouter

from mdm.orders import views

router = DefaultRouter()
router.register(r'compras', views.CompraViewSet)
router.register(r'facturas', views.FacturaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
