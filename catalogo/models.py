from django.db import models
from django.utils import timezone
from django.conf import settings

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
  fecha_registro = models.DateTimeField(default=timezone.localtime)
  activo = models.BooleanField(default=True)

  def __str__(self):
    return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
  
class direccion(models.Model):
  calle = models.CharField(max_length=120)
  numero_exterior = models.CharField(max_length=120)
  numero_interior = models.CharField(max_length=120, blank=True, null=True)
  colonia = models.CharField(max_length=120)
  codigo_postal = models.CharField(max_length=120)
  ciudad = models.CharField(max_length=120)
  estado = models.CharField(max_length=120)
  
  def __str__(self):
    return f"{self.calle} {self.numero_exterior} {self.numero_interior}, Col. {self.colonia}, {self.ciudad}, {self.estado}, CP.  {self.codigo_postal}"

class cliente_direccion(models.Model):
  cliente = models.ForeignKey("cliente", blank=False, null=True, on_delete=models.PROTECT)
  direccion = models.ForeignKey("direccion", blank=False, null=True, on_delete=models.PROTECT)

class tipo_documento(models.Model):
  nombre = models.CharField(max_length=120)
  activo = models.BooleanField(default=True)

class cliente_documentacion(models.Model):
  tipo_documento = models.ForeignKey("tipo_documento", blank=False, null=True, on_delete=models.PROTECT)
  cliente = models.ForeignKey("cliente", blank=False, null=True, on_delete=models.PROTECT)
  archivo = models.FileField(upload_to='cliente_documentos/', blank=True, null=True)
  usuario = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=True, on_delete=models.PROTECT)
  fecha = models.DateTimeField(default=timezone.localtime)

class cliente_referencia(models.Model):
  cliente = models.ForeignKey("cliente", blank=False, null=True, on_delete=models.PROTECT)
  nombre = models.CharField(max_length=120)
  apellido_paterno = models.CharField(max_length=120)
  apellido_materno = models.CharField(max_length=120)
  telefono = models.CharField(max_length=120)
  observaciones = models.TextField(max_length=255)
  valida = models.BooleanField(default=True)
  valida_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=True, on_delete=models.PROTECT) ##si se hace asi??
  valida_fecha = models.DateTimeField(default=timezone.localtime)

class tipo_credito(models.Model):
  tTipo= (
    ('S', 'Semanal'),
    ('M', 'Mensual'),
  )

  tipo = models.CharField(max_length=1, choices=tTipo, default='S')
  nombre = models.CharField(max_length=120)
  duracion = models.FloatField()
  activo = models.BooleanField(default=True)

  def __str__(self):
    return f"{self.nombre} {self.duracion} {self.tipo}"

class tipo_interes(models.Model):
  interes = models.FloatField(default=0)
  factor  = models.FloatField(default=0)
  activo = models.BooleanField(default=True)

  def __str__(self):
    return str(self.interes)

class tipo_interes_factor(models.Model):
  tipo_interes = models.ForeignKey("tipo_interes", blank=False, null=True, on_delete=models.PROTECT)
  no_pago = models.IntegerField(default=1)
  porcentaje_capital = models.FloatField(default=0)
  porcentaje_interes = models.FloatField(default=0)