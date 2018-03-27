from django.contrib import admin
from .models import Owner, Item, Story, Livebox
# Register your models here.
admin.site.register(Owner)
admin.site.register(Item)
admin.site.register(Story)
admin.site.register(Livebox)
