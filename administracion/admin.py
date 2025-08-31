from divox.app.base.utilidades import CustomModelAdmin
from django.contrib import admin

# Register your models here.
class creditoAdmin(CustomModelAdmin):
  list_display = ('id',)