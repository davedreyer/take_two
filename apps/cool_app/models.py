from __future__ import unicode_literals

from django.db import models
from ..log_reg.models import User
from django.db.models import Count

class WishListManager (models.Manager):
	def wishlist_load(self, user_id):
		
		response = {}

		response['wishlist'] = WishListEntry.objects.filter(wisher_id=user_id)
		response['other_wishlist'] = WishListEntry.objects.exclude(wisher_id=user_id)

		return response

class ItemManager (models.Manager):
	def item_check(self, postData, user_id):

		response = {}
			
		error_messages = []	

		if not postData['name']:
			error_messages.append('Item name cannot be blank!')

		elif len(postData['name']) < 3:
			error_messages.append('Item name must contain at least 3 characters!')

		if not error_messages:

			user_obj = User.objects.get(id=user_id) 
			new_item = self.create(name=postData['name'],created_by=user_obj)
			WishListEntry.objects.create(wisher=user_obj,wishitem=new_item)
			response['added'] = True
 
		else:
		
			response['errors'] = error_messages
			response['added'] = False

		return response	
	

	def item_load(self, user_id):

		response = {}

		not_created = Item.objects.exclude(created_by_id=user_id)
		created = Item.objects.filter(created_by_id=user_id)	
		items_all = Item.objects.all()
		not_on_wishlist = []

		for item in items_all:
			query = WishListEntry.objects.filter(wisher_id=user_id).filter(wishitem_id=item.id)
				
			print query.query

			print query

			if not query:
				not_on_wishlist.append(item)

		response['item_not_created'] = not_created
		response['item_created'] = created
		response['items_all'] = items_all
		response['not_on_wishlist'] = not_on_wishlist

		print not_on_wishlist

		return response

class Item(models.Model):
	name = models.CharField(max_length=100)
	created_by=models.ForeignKey(User, related_name="creator")
	created_at = models.DateTimeField(auto_now_add = True)
	objects = ItemManager()
	
class WishListEntry(models.Model):
	wisher=models.ForeignKey(User, related_name="wisher")
	wishitem = models.ForeignKey(Item, related_name="wishitem")
	objects = WishListManager()

	