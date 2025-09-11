from divox.app.base.utilidades import Tabla

class get_integrantes(Tabla):
  app          = "administracion"
  modelo       = "credito_integrante"
  list_hidden  = ['id']
  list_display = ('cliente','monto','acciones')

  def acciones(self, obj):
    credito = obj.credito
    pagos = credito.credito_pago_set.filter(pagado_fecha__isnull=False).exists()

    return {
        'component': 'acciones',
        'props': {
            'hidden': pagos
        }
    }
  acciones.is_component = True