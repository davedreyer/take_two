from django.shortcuts import render, redirect
from django.contrib import messages
from ..log_reg.models import User
from models import Poke
from django.core.urlresolvers import reverse
import datetime
from django.utils import timezone

def index(request):
	
	query = Poke.objects.poke_query(request.session['user']['id'])

	context = {
		'pokee_data': query['pokee_data'],
		'poker_count': query['poker_count'],
		'poker_data': query['poker_data'],
		'user_query': query['user_query']

	}

	return render(request, 'cool_app/index.html', context)

def poke(request):
	if request.method == 'POST':
	
		poker = User.objects.get(id=request.POST['poker'])
		pokee = User.objects.get(id=request.POST['pokee'])
		Poke.objects.create(poker=poker,pokee=pokee)

		return redirect(reverse('cool_app:index'))