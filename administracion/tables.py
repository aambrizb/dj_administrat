from divox.app.base.utilidades import Tabla

class get_integrantes(Tabla):
  app          = "administracion"
  modelo       = "credito_integrante"
  list_hidden  = ['id']
  list_display = ('cliente','monto','acciones',)

  def acciones(self, obj):
        credito = obj.credito
        # Si existe al menos un pago con fecha → deshabilitamos las acciones
        pagos = credito.credito_pago_set.filter(pagado_fecha__isnull=False).exists()
        print("pagos")
        print(pagos)
        if pagos:
          return {
            'component': 'acciones',
            'props': {
              'hidden': True
            }
          }

        return {
          'component': 'acciones'
        }
  acciones.is_component = True

  def get_can_add(self, obj=None):
    if obj.tipo_credito.tipo != 'M':
      return True
    
    if obj and obj.credito.credito_pago_set.filter(pagado_fecha__isnull=False).exists():
      return False
    return True