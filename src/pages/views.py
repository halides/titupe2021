from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from .models import Account

import logging

logger = logging.getLogger(__name__)

@login_required
@csrf_exempt
def transferView(request):
	
	if request.method == 'GET':
		to = User.objects.get(username=request.GET.get('to'))
		amount = int(request.GET.get('amount'))
		request.user.account.balance -= amount
		to.account.balance += amount

		request.user.account.save()
		to.account.save()
	
	return redirect('/')


@login_required
@csrf_exempt
def messageView(request):
	
	if request.method == 'POST':
		from django.db import connection, transaction
		cursor = connection.cursor()
		message = request.POST.get('message')

		cursor.executescript("UPDATE pages_account SET message ='%s' WHERE user_id = 4" % message)
	return redirect('/')


@login_required
@csrf_exempt
def storeSecretsView(request):
	
	if request.method == 'POST':
		secret = request.POST.get('secret')

		request.user.account.secret = secret

		logger.error("I logged secret stuff: " + secret)

		request.user.account.save()
	return redirect('/')


@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})
