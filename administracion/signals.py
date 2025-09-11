from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from administracion.models import credito_integrante,credito_pago
from catalogo.models import tipo_interes_factor
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum

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
  ciclo_obj = _credito.tipo_interes

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

    if ciclo_obj:
    # Obtener tasa y definir factor por tasa
      factor = ciclo_obj.factor

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

  _ultima_fecha  =  _credito.orden_desembolso
  _ultima_fecha  += relativedelta(
    day=_credito.dia_pago, months=1
    if _ultima_fecha.day > _credito.dia_pago else 0)
  # Crear nueva Tabla
  if _credito.tipo_credito.tipo =='M':
    _rango    = range(int(_meses))
    _relative = relativedelta(months=1)
  else:
    _rango    = range(int(_semanas))
    _relative = timedelta(days=7)

  for x in _rango:
    _factor  = tipo_interes_factor.objects.filter(
        tipo_interes = _credito.tipo_interes,
        no_pago      = x+1
    ).last()

    _data = {
      'no_pago'        : x+1,
      'fecha'          : _ultima_fecha,
      'factor_capital' : _factor.porcentaje_capital,
      'factor_interes' : _factor.porcentaje_interes,
      'permite_pagar'  : True if x+1 == 1 else False
    }

    _credito.credito_pago_set.create( **_data )

    _ultima_fecha = _ultima_fecha + _relative

@receiver(post_save, sender=credito_pago)
def update_credito_pago(sender, instance, created, **kwargs):

  if not created and instance.pago:

    monto_total    = instance.credito.monto_total
    monto_pago     = instance.credito.monto_pago
    interes        = instance.credito.monto_interes
    monto_final    = instance.credito.monto_final

    pago = instance.pago
    _factor_capital = instance.factor_capital / 100
    _factor_interes = instance.factor_interes / 100

    _pago_capital    = pago * _factor_capital
    _interes         = pago * _factor_interes
    _subtotal        = _interes / 1.16
    _iva             = _interes - _subtotal
    _saldo_capital   = monto_total - _pago_capital
    _saldo_interes   = interes - _interes
    _cartera_vigente = monto_final - pago
    _capital_mora    = (monto_pago * _factor_capital) - _pago_capital
    _interes_mora    = (monto_pago * _factor_interes) - _interes
    _mora            = _capital_mora + _interes_mora

    _pagado = pago >=monto_pago
    _pagado_fecha = timezone.now()


    credito_pago.objects.filter(pk=instance.pk).update(
      pago_capital    = float('{0:.2f}'.format(_pago_capital)),
      interes         = float('{0:.2f}'.format(_interes)),
      subtotal        = float('{0:.2f}'.format(_subtotal)),
      iva             = float('{0:.2f}'.format(_iva)),
      saldo_capital   = float('{0:.2f}'.format(_saldo_capital)),
      saldo_interes   = float('{0:.2f}'.format(_saldo_interes)),
      cartera_vigente = float('{0:.2f}'.format(_cartera_vigente)),
      capital_mora    = float('{0:.2f}'.format(_capital_mora)),
      interes_mora    = float('{0:.2f}'.format(_interes_mora)),
      mora            = float('{0:.2f}'.format(_mora)),
      pagado          = _pagado,
      pagado_fecha    = _pagado_fecha
    )

    total_mora = instance.credito.credito_pago_set.aggregate(total=Sum('mora'))['total'] or 0

    instance.credito.monto_mora = float('{0:.2f}'.format(total_mora))
    instance.credito.save()