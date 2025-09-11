from django.shortcuts import render
from num2words import num2words
from django.utils import timezone

# Create your views here.
def vista_credito(request,pk=None):
  from administracion.forms import creditoForm
  from administracion.models import credito

  obj = credito.objects.filter(pk=pk).last()

  pagos = False
  if obj:
    pagos = obj.credito_pago_set.filter(pagado_fecha__isnull=False).exists()

  form = creditoForm(request.POST or None,instance=obj)
  if not pagos and form.is_valid():
    obj = form.save()

    # Generar Detalle
    #obj.

  return {
    'custom' : True,
    'form'   : form,
    'obj'    : obj,
    'pagos'  : pagos
  }

def Print_imprimir_estado(request):
  from administracion. models import credito

  pk             = request.POST.get('pk', None)
  obj            = credito.objects.filter(pk=pk).last()
  
  integrantes = obj.credito_integrante_set.all()
  i = integrantes.first()
  if i.cliente:
    cliente_nombre = f"{i.cliente.nombre} {i.cliente.apellido_paterno} {i.cliente.apellido_materno}"


  pagos          = obj.credito_pago_set.all() if obj else []

  mitad          = (len(pagos) + 1) // 2
  primera_mitad  = pagos[:mitad]
  segunda_mitad  = pagos[mitad:]
  return {
    "obj"            : obj,
    "cliente_nombre" : cliente_nombre,
    "primera_mitad"  : primera_mitad,
    "segunda_mitad"  : segunda_mitad,
  }

def numero_a_letras(cantidad):
  try:
    texto = num2words(cantidad, lang='es').replace("uno", "un")
    texto = texto.capitalize() + " pesos"
    return texto
  except:
    return ""

def Print_imprimir_contrato(request):
  from administracion. models import credito
  from catalogo. models import cliente_direccion

  pk             = request.POST.get('pk', None)
  obj            = credito.objects.filter(pk=pk).last()

  integrantes = obj.credito_integrante_set.all()
  i = integrantes.first()

  tipo_credito = obj.tipo_credito
  duracion = tipo_credito.duracion
  
  tipo_plazo = "mensuales" if tipo_credito.tipo == 'M' else "semanales"

  if i.cliente:
    cliente_nombre = f"{i.cliente.nombre} {i.cliente.apellido_paterno} {i.cliente.apellido_materno}"
    
    direccion_obj = cliente_direccion.objects.filter(cliente=i.cliente).select_related('direccion').first()
    cliente_direccion_str = str(direccion_obj.direccion) 

  monto_texto = num2words(obj.monto_total, lang='es').replace("uno", "un").capitalize()
  porcentaje_texto = num2words(obj.tipo_interes.interes, lang='es').replace("uno", "un").capitalize()

  fecha = timezone.localdate()
  fecha_formateada = fecha.strftime("%d de %B del %Y")

  return {
    "obj"               : obj,
    "cliente_nombre"    : cliente_nombre,
    "cliente_direccion" : cliente_direccion_str,
    "monto_texto"       : monto_texto,
    "porcentaje_texto"  : porcentaje_texto,
    "duracion"          : duracion,
    "tipo_plazo"        : tipo_plazo,
    "fecha_formateada"  : fecha_formateada
  }