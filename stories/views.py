from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import QuerySet
from django.views.decorators.csrf import csrf_exempt
from .models import Owner
from .serializer import customEncoder
# Create your views here.

def index(req):
	box_owners = Owner.objects.get(fname='Madi');
	return HttpResponse(str(box_owners.fname));

def addElement(req):
	box_owners = Owner.objects.all();
	listOwners = [];
	for owner in box_owners:
		listOwners.append(str(owner));
	return HttpResponse(str(listOwners));

def getBoxInformation(req):
	box_owners = Owner.objects.all();
	jsonResult = {};
	jsonResult['boxArray'] = serialize('json', box_owners, cls=customEncoder);
	jsonResult['Owner'] = 'Minute Maid';
	jsonResult['Value'] = len(box_owners);
	return JsonResponse(jsonResult);

@csrf_exempt
def compareImage(req):
	data = req.body;
	JSONObjects = serializers.deserialize('json', data);
	print(JSONObjects);
	return HttpResponse("Confirmed");