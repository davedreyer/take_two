from django.shortcuts import render, redirect
from django.contrib import messages
from ..log_reg.models import User
from django.core.urlresolvers import reverse
import datetime
from django.utils import timezone
from models import Item, WishListEntry

def index(request):
	item_load = Item.objects.item_load(request.session['user']['id'])
	wishlist_load = WishListEntry.objects.wishlist_load(request.session['user']['id'])

	context = {
		'item_created' : item_load['item_created'],
		'item_not_created' : item_load['item_not_created'],
		'wishlist' : wishlist_load['wishlist'],
		'other_wishlist' : wishlist_load['other_wishlist'],
		'items_all' : item_load['items_all'],
		'not_on_wishlist' : item_load['not_on_wishlist']
	}

	return render(request, 'cool_app/index.html', context)

def create(request):
	return render(request, 'cool_app/create.html')

def delete_item (request, item_id):
	Item.objects.filter(id=item_id).delete()
	return redirect(reverse('cool_app:dashboard'))

def remove_list (request, item_id):
	WishListEntry.objects.filter(id=item_id).delete()
	return redirect(reverse('cool_app:dashboard'))	

def wish_items (request, item_id):
	wishlist = WishListEntry.objects.filter(wishitem_id=item_id)
	item = Item.objects.get(id=item_id)
	context = {
		'wishlist' : wishlist,
		'item' : item
	}
	return render(request, 'cool_app/wish_items.html', context)	

def add(request):
	if request.method=="POST":
		check = Item.objects.item_check(request.POST, request.session['user']['id'])
		if not check['added']:
			for x in check['errors']:
				messages.error(request, x)

	return redirect(reverse('cool_app:dashboard'))

def add_item(request, item_id):
	user = User.objects.get(id=request.session['user']['id'])
	item = Item.objects.get(id=item_id)
	check = WishListEntry.objects.filter(wisher_id=user.id).filter(wishitem_id=item_id)
	if not check:	
		WishListEntry.objects.create(wishitem=item,wisher=user)

	return redirect(reverse('cool_app:dashboard'))				

	
	