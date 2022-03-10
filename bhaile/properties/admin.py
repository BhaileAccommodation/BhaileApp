from django.contrib import admin
from .models import Post, Booking

# display Posts in admin page
admin.site.register(Post)
admin.site.register(Booking)
