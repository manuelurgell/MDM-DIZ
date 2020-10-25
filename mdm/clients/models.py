from django.db import models


class Cliente(models.Model):
    nombrePila = models.CharField(max_length=30)
    apellidoPat = models.CharField(max_length=30)
    apellidoMat = models.CharField(max_length=30)
    fechaNac = models.DateField()
    genero = models.CharField(max_length=30)


class ClienteInfo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=30, null=True)
    correo = models.EmailField(max_length=30, null=True)
    calle = models.CharField(max_length=50, null=True)
    colonia = models.CharField(max_length=50, null=True)
    cuidad = models.CharField(max_length=50, null=True)
    cp = models.CharField(max_length=10, null=True)
    estado = models.CharField(max_length=50, null=True)
    entreCalles = models.CharField(max_length=50, null=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Clientes Info"


class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField()


class CarritoInfo(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    codigoProductos = models.CharField(max_length=30)
    cantidadProductos = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Carritos Info"
