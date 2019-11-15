from django.contrib import admin
from .models import Post, Tag, Collection, Picture
# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Collection)
admin.site.register(Picture)

