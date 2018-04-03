from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('newEl/',  views.addElement,  name='add'),
	path('getData/',  views.getBoxInformation,  name='getData'),
	path('compareImage/', views.compareImage, name='compareImage'),
]