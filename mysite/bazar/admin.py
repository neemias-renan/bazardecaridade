from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CharityEvent, Item, UserProfile, ReservedItem

class ItemInline(admin.TabularInline):
    model = Item
    extra = 1

class CharityEventAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    extra = 0

class ReservedItemInline(admin.StackedInline):
    model = ReservedItem
    extra = 1

class UserAdmin(UserAdmin):
    inlines = (ProfileInline, ReservedItemInline,)
    extra = 0

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(CharityEvent, CharityEventAdmin)