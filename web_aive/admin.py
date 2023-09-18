from django.contrib import admin

from .models import PrdctnInfo

class PrdctnInfoAdmin(admin.ModelAdmin):
    search_fields = ['prdctn_protein_struct','input_virus_seq_1','input_virus_seq_2','regist_dt']

admin.site.register(PrdctnInfo)
