from divox.app.base.forms import CustomModelForm
from catalogo.models import tipo_credito_ciclo

class tipo_credito_cicloModal(CustomModelForm):
    class Meta:
        model = tipo_credito_ciclo
        exclude = ('tipo_credito',)