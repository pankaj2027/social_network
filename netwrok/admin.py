from django.contrib import admin
from .models import User,Friendship
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'