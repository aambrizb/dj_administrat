from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from administracion.models import credito_integrante, credito
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

@receiver(pre_save, sender=credito_integrante)
def limitar_integrante_credito_mensual(sender, instance, **kwargs):
  credito_obj = instance.credito
  if credito_obj.tipo_credito.tipo == 'M':
    existe = credito_obj.credito_integrante_set.exclude(pk=instance.pk).exists()
    if existe:
      raise ValidationError("Este crédito es tipo individual, solo puede tener un integrante.")

@receiver(post_save, sender=credito_integrante)
def update_capital(sender, **kwargs):
  instance = kwargs.get('instance')

  monto_total = 0

  for item in instance.credito.credito_integrante_set.all():
    monto_total += item.monto

  _credito = instance.credito

  #ciclo asociado al credito
  ciclo_obj = _credito.tasa

  if _credito.tipo_credito.tipo == 'M':
    #Calcular Valores Individuales
    if ciclo_obj:
    # Obtener tasa y definir factor por tasa
      tasa_interes = ciclo_obj.tasa_interes/100

    _meses           = _credito.tipo_credito.duracion
    _interes_mensual = ((monto_total)*tasa_interes)
    _pago_semanal    = (monto_total/_meses)+_interes_mensual
    _interes         = _interes_mensual*_meses
    _total_pagar     = _interes+monto_total


    # Calcular Valores Grupales
  else:

    factor = 72.5  
    if ciclo_obj:
    # Obtener tasa y definir factor por tasa
      tasa_interes = ciclo_obj.tasa_interes

      factores = {
        8: 72.5,
        7: 80.0,
        6: 77.5,
        5: 75.0,
        4: 72.5,
      }

      factor = factores.get(tasa_interes, 72.5)

    _semanas      = _credito.tipo_credito.duracion
    _pago_semanal = (monto_total/1000)*factor
    _interes      = (_pago_semanal*_semanas)-monto_total
    _total_pagar  = _interes+monto_total

  _credito.monto_total   = float('{0:.2f}'.format(monto_total))
  _credito.monto_pago    = float('{0:.2f}'.format(_pago_semanal))
  _credito.monto_interes = float('{0:.2f}'.format(_interes))
  _credito.monto_final   = float('{0:.2f}'.format(_total_pagar))
  _credito.save()

  # Eliminar Corrida Anterior
  _credito.credito_pago_set.all().delete()

  _ultima_fecha = _credito.orden_desembolso+timedelta(days=_credito.dia_pago-1)

  # Crear nueva Tabla
  if _credito.tipo_credito.tipo == 'M':
    for x in range(int(_meses)):
      _credito.credito_pago_set.create(
        no_pago=x+1,
        fecha=_ultima_fecha,
      )

      _ultima_fecha = _ultima_fecha + relativedelta(months=1)
  else:
    for x in range(int(_semanas)):
      _credito.credito_pago_set.create(
        no_pago=x+1,
        fecha=_ultima_fecha,
      )

      _ultima_fecha = _ultima_fecha+timedelta(days=7)

