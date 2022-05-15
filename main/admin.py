from django.contrib import admin

# from .models import Ad, Category, User, Location
from ads.models import Ad, Category
from location.models import Location
from user.models import User

admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Location)
