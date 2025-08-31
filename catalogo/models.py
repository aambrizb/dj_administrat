from django.db import models

# Create your models here.
class tipo_documento(models.Model):
  nombre = models.CharField(max_length=120)
  activo = models.BooleanField(default=True)

  def __str__(self):
    return self.nombre
