#coding: utf-8
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Notification 
from thread import start_new_thread
from models import Payment, Item, Transaction
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test


@csrf_exempt
def notification(request):
	'''
		View responsible for receiving a notification from PagSeguro and make a
		query to update the Payment.
	'''
	incoming_notification = Notification(code=request.POST['notificationCode'])
	incoming_notification.save()
	start_new_thread(incoming_notification.check, tuple())
	return HttpResponse("OK", mimetype="text/plain")

@login_required
@csrf_exempt
def comprar(request, slug):
	if request.POST:
		qtd_ingressos = int(request.POST.get('quantidade_tipo_ingressos'))
		pay = Payment.objects.create(user=request.user)
		for i in range(1,qtd_ingressos+1):
			id_item = int(request.POST.get('tipo_ingresso_' + str(i) ))
			qtd_item = int(request.POST.get('quantidade_ingresso_'+ str(i) ))
			item = get_object_or_404(Item, pk=id_item)
			if not item.tipoingresso.esgotado and qtd_item > 0:
				pay.add_item(item, qtd_item)

		pay.save()		
		pay.submit("http://vainessa.com")
		return redirect(pay.client_url)
	return HttpResponseRedirect(reverse('blog_post_detail', kwargs={'slug':slug}))

@login_required
@csrf_exempt
def finalizar_pagamento(request, pagamento):
	pay = get_object_or_404(Payment, pk=pagamento)
	pay.save()		
	pay.submit("http://vainessa.com")
	return redirect(pay.client_url)


	

