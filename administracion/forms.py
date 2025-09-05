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
      'estado',
    )
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

        # Obtener los valores de tipo_credito y ciclo
    tipo_credito_val = None
    ciclo_val = None

    if 'tipo_credito' in self.data:
        try:
             tipo_credito_val = int(self.data.get('tipo_credito'))
        except (ValueError, TypeError):
            pass

class credito_integranteModal(CustomModelForm):
  class Meta:
    model   = credito_integrante
    exclude = ('credito',)


class credito_abonoForm(CustomModelForm):
    class Meta:
        model = credito_abono
        exclude = ('credito','fecha','usuario',)