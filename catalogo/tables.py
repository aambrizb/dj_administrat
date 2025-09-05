from divox.app.base.utilidades import Tabla

class tipo_interes_factor(Tabla):
    app = "catalogo"
    modelo = "tipo_interes_factor"

    list_display = ('no_pago','porcentaje_capital', 'porcentaje_interes','acciones',)
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

class cliente_referencia(Tabla):
    app = "catalogo"
    modelo = "cliente_referencia"

    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'observaciones', 'valida', 'acciones')
    list_hidden = ['id']

    def acciones(self, obj):
        return {
            'component': 'acciones'
        }
    acciones.is_component = True

class credito_factor(Tabla):
    app = "catalogo"
    modelo = "credito_factor"

    list_display = ('no_pago','porcentaje_capital', 'porcentaje_interes', 'acciones')
    list_hidden = ['id']

    def acciones(self, obj):
        return {
            'component': 'acciones'
        }
    acciones.is_component = True