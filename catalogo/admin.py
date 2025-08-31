from divox.app.base.utilidades import CustomModelAdmin
from django.contrib import admin

# Register your models here.
class tipo_documentoAdmin(CustomModelAdmin):
  list_display = ('id','nombre','activo',)
