from django.core.serializers.json import DjangoJSONEncoder
from .models import Owner, Item, Image, Story, Livebox
from django.db.models import QuerySet
import numpy as np
class customEncoder(DjangoJSONEncoder):
	def default(self, obj):	
		return super().default(obj);

	def fromJSONtoNP(request):
		return np.zeros(1);