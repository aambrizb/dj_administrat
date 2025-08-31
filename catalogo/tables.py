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

class direccion_cliente(Tabla):
    app = "catalogo"
    modelo = "cliente_direccion"

    list_display = ('direccion', 'acciones')
    list_hidden = ['id']

    def acciones(self, obj):
        return {
            'component': 'acciones'
        }
    acciones.is_component = True

class referencia_cliente(Tabla):
    app = "catalogo"
    modelo = "cliente_referencia"

    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'observaciones', 'valida')
    list_hidden = ['id']

    def acciones(self, obj):
        return {
            'component': 'acciones'
        }
    acciones.is_component = True