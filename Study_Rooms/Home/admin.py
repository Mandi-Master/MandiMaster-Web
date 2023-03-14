from django.contrib import admin
from Home.models import Room,Topic,Category,Message
from Home.models import User
# Register your models here.
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Category)
admin.site.register(Message)