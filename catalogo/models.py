from django.db import models
from django.utils import timezone

# Create your models here.
class tipo_documento(models.Model):
  nombre = models.CharField(max_length=120)
  activo = models.BooleanField(default=True)

  def __str__(self):
    return self.nombre

class cliente(models.Model):
  nombre = models.CharField(max_length=120)
  apellido_paterno = models.CharField(max_length=120)
  apellido_materno = models.CharField(max_length=120)
  telefono = models.CharField(max_length=120)
  observaciones = models.TextField(max_length=255)
  direccion= models.ForeignKey("direccion", blank=False, null=True, on_delete=models.PROTECT)
  fecha_registro = models.DateTimeField(default=timezone.localtime)
  activo = models.BooleanField(default=True)

  def __str__(self):
    return self.nombre
  
class direccion(models.Model):
  calle = models.CharField(max_length=120)
  numero_exterior = models.CharField(max_length=120)
  numero_interior = models.CharField(max_length=120)
  colonia = models.CharField(max_length=120)
  codigo_postal = models.CharField(max_length=120)
  ciudad = models.CharField(max_length=120)
  estado = models.CharField(max_length=120)
  
class tipo_credito(models.Model):
  nombre = models.CharField(max_length=120)
  meses = models.FloatField()
  activo = models.BooleanField(default=True)

  def __str__(self):
    return self.nombre

class tipo_credito_ciclo(models.Model):
  tipo_credito = models.ForeignKey("tipo_credito", blank=False, null=False, on_delete=models.PROTECT)
  ciclo = models.IntegerField()
  tasa_interes = models.FloatField()