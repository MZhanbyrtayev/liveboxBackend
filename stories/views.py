from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import QuerySet
from django.views.decorators.csrf import csrf_exempt
from .models import Owner, Livebox, Image, BoxStory, Item, Story
from .serializer import customEncoder
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import VGG16, decode_predictions, preprocess_input
import cv2
import numpy as np
import json
global model;
model = VGG16();
model._make_predict_function();
# Create your views here.
def index(req, id):
	box = Livebox.objects.get(pk=id);
	print(box);
	bstory = BoxStory.objects.filter(parent_box=box);
	bstory = bstory.first();
	print(bstory);
	return FileResponse(bstory.audio_path);

def addElement(req):
	box_owners = Owner.objects.all();
	listOwners = [];
	for owner in box_owners:
		listOwners.append(str(owner));
	return HttpResponse(str(listOwners));

def getFile(req,id):	
	bstory = Story.objects.filter(pk=id);
	bstory = bstory.first();
	return FileResponse(bstory.audio_path);

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
	dictionary['box'] = liveboxes.pk;
	print(dictionary);
	return JsonResponse(dictionary);

@csrf_exempt
def compareImage(req):
	jsonDictionary = json.loads(req.body.decode('utf-8'));
	#print(jsonDictionary);
	mat = np.array(jsonDictionary['Matrix']);
	#img = np.ndarray(mat,mat,mat);
	print(mat.shape);
	#img = cv2.createMat(h,w,cv2.CV_32FC3);
	#cv2.imwrite('newmedia.png', mat);
	orb = cv2.ORB_create();
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True);
	imageFrames = Image.objects.all();
	numImages = len(imageFrames);
	print(numImages)
	results=[];
	for im2 in imageFrames:
		path = str(im2.image_src);
		im = cv2.imread('media/'+path,0);
		print(im.shape)
		#cv2.imwrite('n2.png', im);
		imageDict={};
		kp, des = orb.detectAndCompute(im, None);
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

@csrf_exempt
def checkKeras(req):
	
	jsonDictionary = json.loads(req.body.decode('utf-8'));
	mat = np.array(jsonDictionary['Matrix']);
	print(mat.shape);
	#cv2.imwrite('res.png', mat);
	newarr = np.ndarray(shape=(224,224,3),dtype=np.float64);
	for i in range(0,224):
		for j in range(0,224):
			newarr[i,j]=[mat[i,j],mat[i,j],mat[i,j]];
	#rgb = np.array([mat, mat, mat]);
	cv2.imwrite('res.png', newarr);
	mat = img_to_array(newarr);
	mat = mat.reshape((1,mat.shape[0],mat.shape[1],mat.shape[2]));
	#print(image.shape);
	image = mat;
	image = preprocess_input(image);
	yhat = model.predict(image);
	labels = decode_predictions(yhat);

	print(labels[0][0:5]);
	items = Item.objects.all();
	for item in items:
		for i in range(0, len(labels)):
			s = labels[0][i][1];
			print(s);
			if s in item.item_label:
				stories = Story.objects.filter(parent_item=item);
				print(stories);
				story = stories.first();
				dictionary ={};
				dictionary['item_pk']=story.pk;
				return JsonResponse(dictionary);


	return HttpResponse("Confirmed");