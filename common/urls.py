from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup', views.signup, name='signup'),
    path('sitemap', views.sitemap, name="sitemap"),
    path('get_domain_seq_info', views.get_domain_seq_info, name='get_domain_seq_info'),
    path('get_comm_code_list', views.get_comm_code_list, name='get_comm_code_list'),
    path('get_comm_post_request', views.get_comm_post_request, name="get_comm_post_request"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
]

app_name = 'common'