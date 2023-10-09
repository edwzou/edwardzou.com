from django.contrib import admin
from . models import Feedback

# Update Admin Panel - Header
admin.site.site_header = "Backend - CVAPP - edwardzou.com"
admin.site.site_title = "Feedback Admin Area"
admin.site.index_title = "Welcome to the Feedback Admin, Backend of edwardzou.com"

# Register your models here.
admin.site.register(Feedback)
# list_display = ("name", "email")
