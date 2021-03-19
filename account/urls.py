from django.conf.urls import url
from django.urls import reverse_lazy

from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    # url(r'^login/$', views.user_login, name="user_login"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html'), name="user_login"),
    url(r'^new/$', auth_views.LoginView.as_view(template_name='account/login.html'), name="user_login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name="user_logout"),
    url(r'^register/$', views.register, name="user_register"),
    url(r'^password-change/$', auth_views.PasswordChangeView.as_view(template_name=
                                                                     'registration/password_change_form.html',
                                                                     success_url=reverse_lazy(
                                                                         'account:password_change_done')),
        name='password_change'),
    url(r'^password-change/$', auth_views.PasswordChangeDoneView.as_view(template_name=
                                                                         'registration/password_change_done.html'),
        name='password_change'),
]
