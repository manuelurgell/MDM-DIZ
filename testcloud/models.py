from django.db import models


class Cliente(models.Model):
    nombrePila = models.CharField(max_length=30)
    apellidoPat = models.CharField(max_length=30)
    apellidoMat = models.CharField(max_length=30)
    fechaNac = models.DateField()
    genero = models.CharField(max_length=30)


class ClienteInfo(models.Model):
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=30, null=True)
    correo = models.EmailField(max_length=30, null=True)
    calle = models.CharField(max_length=50, null=True)
    colonia = models.CharField(max_length=50, null=True)
    cuidad = models.CharField(max_length=50, null=True)
    cp = models.CharField(max_length=10, null=True)
    estado = models.CharField(max_length=50, null=True)
    entreCalles = models.CharField(max_length=50, null=True)


class CarritoAbandonado(models.Model):
    idCarrito = models.CharField(max_length=30, primary_key=True)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()


class CaritoInfo(models.Model):
    idCarrito = models.ForeignKey(CarritoAbandonado, on_delete=models.CASCADE)
    codigoProductos = models.CharField(max_length=30)
    cantidadProductos = models.CharField(max_length=30)


class Compra(models.Model):
    idCompra = models.CharField(max_length=30, primary_key=True)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    noTarjeta = models.CharField(max_length=30)
    fecha = models.DateField()
    hora = models.CharField(max_length=30)
    total = models.CharField(max_length=50)
    calle = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    colonia = models.CharField(max_length=50)
    cuidad = models.CharField(max_length=50)
    cp = models.CharField(max_length=10)
    estado = models.CharField(max_length=50)
    entreCalles = models.CharField(max_length=50)


class Pedido(models.Model):
    idCompra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    codigoProductos = models.CharField(max_length=30)
    cantidadProductos = models.CharField(max_length=30)
    precioProductos = models.CharField(max_length=30)


class Factura(models.Model):
    idCompra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    RFC = models.CharField(max_length=30)
    razonSocial = models.CharField(max_length=30)
    fecha = models.DateField()
    correo = models.EmailField(max_length=30)
    telefono = models.CharField(max_length=30)
    calle = models.CharField(max_length=50)
    numero = models.CharField(max_length=30)
    colonia = models.CharField(max_length=50)
    cuidad = models.CharField(max_length=50)
    cp = models.CharField(max_length=10)
    estado = models.CharField(max_length=50)
    entreCalles = models.CharField(max_length=50)
