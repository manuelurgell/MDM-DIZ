from django.db import models


class Cliente(models.Model):
    nombrePila = models.CharField(max_length=30)
    apellidoPat = models.CharField(max_length=30)
    apellidoMat = models.CharField(max_length=30)
    fechaNac = models.DateField()
    genero = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)


class ClienteInfo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=30, null=True, default='')
    correo = models.EmailField(max_length=30, null=True, default='')
    calle = models.CharField(max_length=50, null=True, default='')
    colonia = models.CharField(max_length=50, null=True, default='')
    cuidad = models.CharField(max_length=50, null=True, default='')
    cp = models.CharField(max_length=10, null=True, default='')
    estado = models.CharField(max_length=50, null=True, default='')
    entreCalles = models.CharField(max_length=50, null=True, default='')
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Clientes Info"


class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "-fecha"


class CarritoInfo(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    codigoProductos = models.CharField(max_length=30)
    cantidadProductos = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Carritos Info"
