from django.contrib import admin

from .models import CommCode

class CommCodeAdmin(admin.ModelAdmin):
    search_fields = ['cl_code','cl_code_nm','code','code_nm']
    list_display = ('cl_code','cl_code_nm','code','code_nm')

admin.site.register(CommCode, CommCodeAdmin)
