from django.core.serializers.json import DjangoJSONEncoder
from .models import Owner, Item, Image, Story, Livebox
from django.db.models import QuerySet
class customEncoder(DjangoJSONEncoder):
	def default(self, obj):
		if isinstance(obj, QuerySet):
			result = [];
			for q in QuerySet:
				if isinstance(q, Owner):
					result.append({'private_key':q.pk, 'fname': q.fname, 'lname':q.lname});
			return str(obj);
		elif isinstance(obj, Item):

			return str(obj);
		return super().default(obj);