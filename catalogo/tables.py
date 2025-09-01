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

class cliente_direccion(Tabla):
    app = "catalogo"
    modelo = "cliente_direccion"

    list_display = ('direccion', 'acciones',)
    list_hidden = ['id']

    def acciones(self, obj):
        return {
            'component': 'acciones'
        }
    acciones.is_component = True

class cliente_documentacion(Tabla):
    app = "catalogo"
    modelo = "cliente_documentacion"

    list_display = ('tipo_documento', 'archivo', 'acciones',)
    list_hidden = ['id']

    def acciones(self, obj):
        return {
            'component': 'acciones'
        }
    acciones.is_component = True

class referencia_cliente(Tabla):
    app = "catalogo"
    modelo = "cliente_referencia"

    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'observaciones', 'valida', 'acciones')
    list_hidden = ['id']

    def acciones(self, obj):
        return {
            'component': 'acciones'
        }
    acciones.is_component = True