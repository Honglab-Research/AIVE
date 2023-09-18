from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'aive'

urlpatterns = [
    path('', views.aive_main, name='main'),
    path('main', views.aive_main, name='main'),
    path('prdctn_regist_server', views.prdctn_regist_server, name='prdctn_regist_server'),
    path('prdctn_regist_colab', views.prdctn_regist_colab, name='prdctn_regist_colab'),
    path('prdctn_insert', views.prdctn_insert, name='prdctn_insert'),
    path('prdctn_list', views.prdctn_list, name='prdctn_list'),
    path('prdctn_result/<int:prdctn_info_seq>', views.prdctn_result, name='prdctn_result'),
    path('prdctn_result_compare', views.prdctn_result_compare, name='prdctn_result_compare'),
    path('filedownload', views.file_download, name='filedownnload'),
    path('prdctn_result_download', views.prdctn_result_download, name='prdctn_result_download'),
    path('aive_result_viewer', views.aive_result_viewer, name='aive_result_viwer'),
    path('get_pdockq', views.get_pdockq, name="get_pdockq"),
    path('get_apess_result', views.get_apess_result, name="get_apess_result"),
    path('apes_view', views.apes_view, name="apes_view"),
    path('aive_about', views.aive_about, name="aive_about"),
    path('aive_tutorial', views.aive_tutorial, name="aive_tutorial"),
]
