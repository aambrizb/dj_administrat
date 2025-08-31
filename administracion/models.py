from django.db import models
from django.utils import timezone

# Create your models here.
class credito(models.Model):

  tEstado = (
    ('A','Activo'),
    ('F', 'Finalizado'),
  )

  fecha            = models.DateTimeField(default=timezone.localtime)
  tipo_credito     = models.ForeignKey('catalogo.tipo_credito', blank=True, null=True, on_delete=models.PROTECT)
  nombre           = models.CharField(max_length=120)
  monto_total      = models.FloatField(default=0)
  monto_pago       = models.FloatField(default=0)
  monto_mora       = models.FloatField(default=0)
  monto_interes    = models.FloatField(default=0)
  monto_final      = models.FloatField(default=0)
  plazo            = models.IntegerField(default=0)
  dia_pago         = models.IntegerField()
  orden_desembolso = models.DateField()
  ciclo            = models.IntegerField(default=1)
  cantidad_pagos   = models.IntegerField(default=0)
  pagos_realizados = models.IntegerField(default=0)
  estado           = models.CharField(max_length=1,choices=tEstado,default='A')

class credito_integrante(models.Model):
  credito = models.ForeignKey('credito',blank=True,null=True,on_delete=models.PROTECT)
  cliente = models.ForeignKey('catalogo.cliente', blank=True, null=True, on_delete=models.PROTECT)
  monto   = models.FloatField(default=0)

class credito_pago(models.Model):
  credito         = models.ForeignKey('credito', blank=True, null=True, on_delete=models.PROTECT)
  no_pago         = models.IntegerField(default=1)
  fecha           = models.DateField()
  pago_capital    = models.FloatField(default=0)
  interes         = models.FloatField(default=0)
  subtotal        = models.FloatField(default=0)
  iva             = models.FloatField(default=0)
  pago            = models.FloatField(default=0)
  saldo_capital   = models.FloatField(default=0)
  saldo_interes   = models.FloatField(default=0)
  cartera_vigente = models.FloatField(default=0)
  capital_mora    = models.FloatField(default=0)
  interes_mora    = models.FloatField(default=0)
  mora            = models.FloatField(default=0)
  pagado          = models.BooleanField(default=False)
  pagado_fecha    = models.DateTimeField(blank=True,null=True)

class credito_abono(models.Model):
  credito = models.ForeignKey('credito',blank=True,null=True,on_delete=models.PROTECT)
  fecha   = models.DateTimeField(default=timezone.localtime)
  usuario = models.ForeignKey('usuario.usuario',blank=True,null=True,on_delete=models.PROTECT)
  monto   = models.FloatField(default=0)


