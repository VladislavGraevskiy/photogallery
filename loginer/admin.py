from loginer.models import User
from django.contrib import admin


def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()
upper_case_name.short_description = 'Name'


class UsersAdmin (admin.ModelAdmin):
    #fields = ['last_name', 'first_name']
    list_display = (upper_case_name, 'data_of_reg','nikname')
    list_filter = ['data_of_reg']
    search_fields = ['last_name']
    date_hierarchy = 'data_of_reg'
admin.site.register(User, UsersAdmin)

# Register your models her