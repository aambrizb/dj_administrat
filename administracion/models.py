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
  tipo_interes     = models.ForeignKey('catalogo.tipo_interes', blank=True, null=True, on_delete=models.PROTECT)
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

  def can_add(self):
    if self.tipo_credito.tipo != 'M':
      return True
    pagos_existen = self.credito_pago_set.filter(pagado_fecha__isnull=False).exists()
    return not pagos_existen

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
  factor_capital  = models.FloatField(default=0)
  factor_interes  = models.FloatField(default=0)
  permite_pagar   = models.BooleanField(default=False)

class credito_abono(models.Model):
  credito = models.ForeignKey('credito',blank=True,null=True,on_delete=models.PROTECT)
  fecha   = models.DateTimeField(default=timezone.localtime)
  usuario = models.ForeignKey('usuario.usuario',blank=True,null=True,on_delete=models.PROTECT)
  monto   = models.FloatField(default=0)

class abono_relacion(models.Model):
  credito_abono = models.ForeignKey('credito_abono', blank=True, null=True, on_delete=models.PROTECT)
  credito_pago  = models.ForeignKey('credito_pago', blank=True, null=True, on_delete=models.PROTECT)
