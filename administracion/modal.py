
def pagar(request,app,popup):
  from administracion.forms import credito_abonoForm
  from administracion.models import credito_pago

  saved = False
  pk = request.GET.get('pk')
  credito_id = request.GET.get('credito_id')

  obj_credito = credito_pago.objects.filter(pk = pk).last()

  form = credito_abonoForm(request.POST or None)

  if form.is_valid():
    obj = form.save()

    obj.credito_id = credito_id
    obj.save()
    obj_credito.pago = obj.monto
    obj_credito.save()

    saved = True
    print (obj)

  return {
    'form':form,
    'saved':saved
  }