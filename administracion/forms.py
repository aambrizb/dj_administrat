from divox.app.base.forms import CustomModelForm
from administracion.models import credito, credito_integrante, credito_abono
from catalogo.models import tipo_credito_ciclo

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

    if 'ciclo' in self.data:
        try:
            ciclo_val = int(self.data.get('ciclo'))
        except (ValueError, TypeError):
            pass

        # Para edición de un objeto existente
    if self.instance.pk:
        if self.instance.tipo_credito:
            tipo_credito_val = self.instance.tipo_credito.id
        if self.instance.ciclo:
            ciclo_val = self.instance.ciclo

        # Filtrar queryset de tasa según tipo_credito y ciclo
    if tipo_credito_val is not None and ciclo_val is not None:
        self.fields['tasa'].queryset = tipo_credito_ciclo.objects.filter(
            tipo_credito_id=tipo_credito_val,
            ciclo=ciclo_val
        )
    else:
        self.fields['tasa'].queryset = tipo_credito_ciclo.objects.none()

class credito_integranteModal(CustomModelForm):
  class Meta:
    model   = credito_integrante
    exclude = ('credito',)


class credito_abonoForm(CustomModelForm):
    class Meta:
        model = credito_abono
        exclude = ('credito','fecha','usuario',)