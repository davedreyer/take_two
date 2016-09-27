from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^dashboard$', views.index,name='dashboard'),
	url(r'^create$', views.create,name='create'),
	url(r'^add_item/(?P<item_id>\d+)$', views.add_item,name='add_item'),
	url(r'^delete_item/(?P<item_id>\d+)$', views.delete_item,name='delete_item'),
	url(r'^remove_list/(?P<item_id>\d+)$', views.remove_list,name='remove_list'),
	url(r'^wish_items/(?P<item_id>\d+)$', views.wish_items,name='wish_items'),
	url(r'^add$', views.add,name='add'),
	url(r'^$', views.index,name='index')
]