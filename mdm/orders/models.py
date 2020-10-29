from django.db import models
from mdm.clients.models import Cliente


class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    noTarjeta = models.CharField(max_length=30)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.CharField(max_length=50)
    calle = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    colonia = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    cp = models.CharField(max_length=10)
    estado = models.CharField(max_length=50)
    entreCalles = models.CharField(max_length=50)


class Pedido(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='pedido'
    )
    codigoProducto = models.CharField(max_length=30)
    cantidadProducto = models.CharField(max_length=30)
    precioProducto = models.CharField(max_length=30)


class Factura(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    RFC = models.CharField(max_length=30)
    razonSocial = models.CharField(max_length=30)
    fecha = models.DateTimeField(auto_now_add=True)
    correo = models.EmailField(max_length=30)
    telefono = models.CharField(max_length=30)
    calle = models.CharField(max_length=50)
    numero = models.CharField(max_length=30)
    colonia = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    cp = models.CharField(max_length=10)
    estado = models.CharField(max_length=50)
    entreCalles = models.CharField(max_length=50)
