from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class CodigoPostal(models.Model):
    codigo = models.CharField(max_length=7)
    colonia = models.CharField(max_length=100)
    municipio = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Codigos postales"
        ordering = ['id']


class NameException(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Excepciones"


class Cliente(models.Model):
    nombrePila = models.CharField(max_length=30)
    apellidoPat = models.CharField(max_length=30)
    apellidoMat = models.CharField(max_length=30)
    fechaNac = models.DateField()
    genero = models.CharField(max_length=1)
    created_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)


class ClienteInfo(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='clienteInfo'
    )
    telefono = PhoneNumberField(
        max_length=12, null=True, blank=True, default=''
    )
    correo = models.EmailField(
        max_length=30, null=True, blank=True, default=''
    )
    noTarjeta = models.CharField(
        max_length=30, null=True, blank=True, default=''
    )
    mesTarjeta = models.CharField(
        max_length=2, null=True, blank=True, default=''
    )
    anioTarjeta = models.CharField(
        max_length=2, null=True, blank=True, default=''
    )
    calle = models.CharField(
        max_length=50, null=True, blank=True, default=''
    )
    colonia = models.CharField(
        max_length=50, null=True, blank=True, default=''
    )
    ciudad = models.CharField(
        max_length=50, null=True, blank=True, default=''
    )
    cp = models.CharField(
        max_length=10, null=True, blank=True, default=''
    )
    estado = models.CharField(
        max_length=50, null=True, blank=True, default=''
    )
    entreCalles = models.CharField(
        max_length=50, null=True, blank=True, default=''
    )
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Clientes_Info"


class Carrito(models.Model):
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        primary_key=True
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "-fecha"


class CarritoInfo(models.Model):
    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        related_name='carritoInfo'
    )
    codigoProducto = models.CharField(max_length=30)
    cantidadProducto = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Carritos_Info"
