from django.db import models
import cv2
import numpy as np
# Create your models here.

#Owner - owner of a livebox
#fname - first
#lname - last name
class Owner(models.Model):
	class Meta:
		verbose_name_plural = 'Owners';
	fname = models.CharField(max_length=30);
	lname = models.CharField(max_length=30);
	birth_date =  models.DateField();

	def __str__(self):
		return str(self.fname+" "+self.lname)+", Date of Birth: "+str(self.birth_date);

# Livebox model
# The model of a livebox which contains
class Livebox(models.Model):
	class Meta:
		verbose_name_plural = 'Liveboxes';

	capacity = models.IntegerField(default=0);
	bluetooth_device = models.CharField(max_length=50);
	box_owner = models.ForeignKey(Owner, on_delete=models.CASCADE);

	def __str__(self):
		return str(self.box_owner)+", Device:"+self.bluetooth_device;
# Physical item to be scanned
# name - may be defined as type, but mostly for presentation
# purposes
# id - unique ID
# owner - individual to whom this item belongs 1 owner
class Item(models.Model):
	class Meta:
		verbose_name_plural = 'Items';
	item_name = models.CharField(max_length=30);
	item_box = models.ForeignKey(Livebox, on_delete=models.CASCADE);
	item_label = models.CharField(max_length=30);

	def __str__(self):
		return str(self.item_name);

class Image(models.Model):
	class Meta:
		verbose_name_plural = 'Images';

	image_src = models.ImageField(default='');
	parent_item = models.ForeignKey(Item, on_delete=models.CASCADE);


	def __str__(self):
		return 'Image parent is '+str(self.parent_item);

# The story - either visual or audio accompaniement
# title - title of the story
# type - audio or video
# path - the file path
# parent_item - the item this story is about
class Story(models.Model):
	class Meta:
		verbose_name_plural = 'Stories'

	title = models.CharField(max_length=50);
	audio_path = models.FileField();
	video_path = models.FileField();	
	parent_item = models.ForeignKey(Item, on_delete=models.CASCADE);

	def __str__(self):
		return str(self.title);


class BoxStory(models.Model):
	class Meta:
		verbose_name_plural = 'Box Stories';

	title =  models.CharField(max_length=50);
	audio_path = models.FileField();
	video_path = models.FileField();
	parent_box = models.ForeignKey(Livebox, on_delete=models.CASCADE);

