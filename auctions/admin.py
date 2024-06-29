from django.contrib import admin

from .models import Bid, Listing, User, Comment

class UserAdmin(admin.ModelAdmin):
    """Contains User model admin page config"""
    list_display = ("id", "username", "email")

admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)