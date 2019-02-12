from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers

from jira.views import Jira, UserData

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="base.html")),
]

router = routers.SimpleRouter()

router.register(r'jira', Jira, base_name='jira')
router.register(r'user', UserData, base_name='user')

urlpatterns += router.urls