from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mdm.orders import views

router = DefaultRouter()
router.register(r'compras', views.CompraViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
