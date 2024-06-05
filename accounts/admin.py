from django.contrib import admin
from.models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display= ['first_name','last_name','username','email','phn_number','date_joined','last_login']
    list_display_links = ('first_name','last_name','username','email')
    readonly_fields = ('date_joined','last_login')
    ordering= ('-date_joined',)
    

    filter_horizontal=()
    list_filter=()
    fieldsets=()

admin.site.register(Account,AccountAdmin)