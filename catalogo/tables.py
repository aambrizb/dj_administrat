from divox.app.base.utilidades import Tabla

class tipo_ciclo(Tabla):
    app = "catalogo"
    modelo = "tipo_credito_ciclo"

    list_display = ('ciclo', 'tasa_interes','acciones',)
    list_hidden = ['id']

    def acciones(self, obj):
        return {
            'component': 'acciones'
        }
    acciones.is_component = True