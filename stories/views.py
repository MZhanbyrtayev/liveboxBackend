from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import QuerySet
from django.views.decorators.csrf import csrf_exempt
from .models import Owner, Livebox, Image
from .serializer import customEncoder
import cv2
import numpy as np
import json
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

@csrf_exempt
def getBoxInformation(req):
	jsonDictionary = json.loads(req.body.decode('utf-8'));
	liveboxes = Livebox.objects.get(bluetooth_device=jsonDictionary['Address']);
	owners = Owner.objects.filter(pk=liveboxes.box_owner.pk);
	owner = owners.first();
	print(owner);
	dictionary = {};
	dictionary['name'] = owner.fname;
	dictionary['lname'] = owner.lname;
	dictionary['DoB'] = owner.birth_date;
	dictionary['box_capacity'] = liveboxes.capacity;
	return JsonResponse(dictionary);

@csrf_exempt
def compareImage(req):
	jsonDictionary = json.loads(req.body.decode('utf-8'));
	#print(jsonDictionary);
	mat = np.array(jsonDictionary['Matrix']);

	FLANN_INDEX_KDTREE = 0;
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5);
	search_params = dict(checks = 50);
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True);
	orb = cv2.ORB_create();
	imageFrames = Image.objects.all();
	numImages = len(imageFrames);
	results=[];
	for im2 in imageFrames:
		path = str(im2.image_src);
		im = cv2.imread(path,0);
		imageDict={};
		kp = orb.detect(im, None);
		kp, des = orb.compute(im, kp);
		matches = bf.match(mat,des);
		goodMatches = [];
		total = 0;
		for m,n in matches:
			total += 1 ;
			if m.distance < 0.7*n.distance:
				goodMatches.append(m);

		imageDict['total'] = total;
		imageDict['good'] = len(goodMatches);
		imageDict['image'] = str(im.parent_item);
		results.append(imageDict);
	print(results);
	return HttpResponse("Confirmed");
