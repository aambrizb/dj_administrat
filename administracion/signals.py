from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from administracion.models import credito_integrante
from datetime import timedelta

@receiver(post_save, sender=credito_integrante)
def update_capital(sender, **kwargs):
  instance = kwargs.get('instance')

  monto_total = 0

  for item in instance.credito.credito_integrante_set.all():
    monto_total += item.monto

  _credito = instance.credito

  # Calcular Valores
  _semanas      = _credito.tipo_credito.meses*4
  _pago_semanal = (monto_total/1000)*72.50
  _interes      = (_pago_semanal*_semanas)-monto_total
  _total_pagar  = _interes+monto_total

  _credito.monto_total   = float('{0:.2f}'.format(monto_total))
  _credito.monto_pago    = float('{0:.2f}'.format(_pago_semanal))
  _credito.monto_interes = float('{0:.2f}'.format(_interes))
  _credito.monto_final   = float('{0:.2f}'.format(_total_pagar))
  _credito.save()

  # Eliminar Corrida Anterior
  _credito.credito_pago_set.all().delete()

  _ultima_fecha = _credito.orden_desembolso+timedelta(days=_credito.dia_pago)

  # Crear nueva Tabla
  for x in range(int(_semanas)):
    _credito.credito_pago_set.create(
      no_pago=x+1,
      fecha=_ultima_fecha,
    )

    _ultima_fecha = _ultima_fecha+timedelta(days=5)

