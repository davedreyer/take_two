from __future__ import unicode_literals

from django.db import models
from ..log_reg.models import User
from django.db.models import Count

class PokeManager(models.Manager):	
	def poke_query(self, user_id):

		response = {}

		poker_count = Poke.objects.filter(pokee_id=user_id).values('poker_id').distinct().count()

		poker_data = Poke.objects.filter(pokee_id=user_id).values('poker_id').annotate(total=Count('poker_id'))

		pokee_data = User.objects.exclude(id=user_id).values('pokee__pokee_id').annotate(total=Count('pokee__pokee_id'))

		user_query = User.objects.all()

		response['poker_data'] = poker_data
		response['poker_count'] = poker_count
		response['pokee_data'] = pokee_data
		response['user_query'] = user_query

		print pokee_data

		print pokee_data.query

		return response

class Poke(models.Model):
	poker=models.ForeignKey(User, related_name="poker")
	pokee=models.ForeignKey(User, related_name="pokee")
	created_at = models.DateTimeField(auto_now_add = True)
	objects = PokeManager()