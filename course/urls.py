from django.conf.urls import url
from django.views.generic import TemplateView
from .views import AboutView

urlpatterns = [
     # url(r'about/$', TemplateView.as_view(template_name="course/about.html")),
     url(r'about/$', AboutView.as_view(), name="about"),
]
