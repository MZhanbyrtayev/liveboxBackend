from django.urls import path
from . import views

urlpatterns = [
	path('<int:id>/', views.index),
	path('newEl/',  views.addElement,  name='add'),
	path('getData/',  views.getBoxInformation,  name='getData'),
	path('compareImage/', views.compareImage, name='compareImage'),
	path('getFile/<int:id>/', views.getFile),
	path('checkKeras/', views.checkKeras),
]