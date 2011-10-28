from django.contrib import admin
from customize.models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    ''
    list_display = ['ulogin', 'country', 'city', 'bdate']

admin.site.register(UserInfo, UserInfoAdmin)
