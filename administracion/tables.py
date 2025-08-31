from divox.app.base.utilidades import Tabla

class get_integrantes(Tabla):
  app          = "administracion"
  modelo       = "credito_integrante"
  list_hidden  = ['id']
  list_display = ('cliente','monto','acciones',)

  def acciones(self,obj):
    return {
      'component':'acciones'
    }

  acciones.is_component = True