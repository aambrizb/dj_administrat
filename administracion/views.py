from django.shortcuts import render

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
