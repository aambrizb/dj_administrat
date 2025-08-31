from divox.app.base.forms import CustomModelForm
from catalogo.models import tipo_credito_ciclo, cliente, cliente_referencia, cliente_direccion

class tipo_credito_cicloModal(CustomModelForm):
    class Meta:
        model = tipo_credito_ciclo
        exclude = ('tipo_credito',)

class cliente_direccionModal(CustomModelForm):
    class Meta:
        model = cliente_direccion
        exclude = ('cliente',)

class clienteForm(CustomModelForm):
    class Meta:
        model = cliente
        exclude = ('fecha_registro',)

class cliente_referenciaModal(CustomModelForm):
    class Meta:
        model = cliente_referencia
        exclude = ('cliente', 'fecha_registro', 'valida_usuario', 'valida_fecha')