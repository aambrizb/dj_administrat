from divox.app.base.utilidades import CustomModelAdmin
from django.contrib import admin

# Register your models here.
class tipo_documentoAdmin(CustomModelAdmin):
  list_display = ('id','nombre','activo',)

class clienteAdmin(CustomModelAdmin):
  list_display = ('id','nombre','activo',)

class tipo_creditoAdmin(CustomModelAdmin):
  list_display = ('id','nombre', 'duracion', 'tipo', 'activo',)

class tipo_interesAdmin(CustomModelAdmin):
  list_display = ('id','interes','activo',)

