from django.contrib import admin
from .models import Owner, Item, Story, Livebox, Image, BoxStory
# Register your models here.
admin.site.register(Owner)
admin.site.register(Item)
admin.site.register(Story)
admin.site.register(Livebox)
admin.site.register(Image)
admin.site.register(BoxStory)