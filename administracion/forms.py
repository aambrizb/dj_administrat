from divox.app.base.forms import CustomModelForm
from administracion.models import credito, credito_integrante, credito_abono


class creditoForm(CustomModelForm):
  class Meta:
    model = credito
    exclude = (
      'fecha',
      'monto_total',
      'monto_pago',
      'monto_mora',
      'monto_interes',
      'monto_final',
      'plazo',
      'ciclo',
      'cantidad_pagos',
      'pagos_realizados',
      'estado'
    )

class credito_integranteModal(CustomModelForm):
  class Meta:
    model   = credito_integrante
    exclude = ('credito',)


class credito_abonoForm(CustomModelForm):
    class Meta:
        model = credito_abono
        exclude = ('credito','fecha','usuario',)