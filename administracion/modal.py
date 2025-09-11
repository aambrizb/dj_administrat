
def pagar(request,app,popup):
  from administracion.forms import credito_abonoForm
  from administracion.models import credito_pago
  from django.db.models import Q

  saved = False
  pk = request.GET.get('pk')
  credito_id = request.GET.get('credito_id')

  obj_credito_pago = credito_pago.objects.filter(pk = pk).last()
  obj_credito      = obj_credito_pago.credito

  form = credito_abonoForm(request.POST or None)

  if form.is_valid():
    obj = form.save()

    obj.credito_id = credito_id
    obj.save()

    _pago            = obj.monto
    ultimo_pendiente = None
    primer_pendiente = None
    total_pago       = 0

    while _pago > 0 :
      pendiente   = obj_credito.credito_pago_set.filter(pago__lt = obj_credito.monto_pago ).first()
      faltante    = obj_credito.monto_pago - pendiente.pago
      _pago_final = faltante if _pago >= faltante else _pago


      pendiente.pago += _pago_final
      pendiente.permite_pagar = False
      pendiente.save()

      ultimo_pendiente = pendiente

      _pago -= _pago_final

      total_pago += 1

      if total_pago == 1:
        primer_pendiente = pendiente
     
    qs_pendiente            = obj_credito.credito_pago_set.filter( Q(pago = 0) | Q(pago__lte = obj_credito.monto_pago)).exclude(pagado =True).exclude(pk = primer_pendiente.id)
    if ultimo_pendiente.pago == obj_credito.monto_pago :
      qs_pendiente = qs_pendiente.exclude(pk = ultimo_pendiente.id)

    pendiente = qs_pendiente.first()

    pendiente.permite_pagar = True
    pendiente.save()

    saved = True

  return {
    'form':form,
    'saved':saved
  }