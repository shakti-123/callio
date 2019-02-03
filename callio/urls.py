from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers

from fibonacci.views import Fibonacci

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="base.html")),
]

router = routers.SimpleRouter()

router.register(r'fibonacci', Fibonacci, base_name='fibonacci')

urlpatterns += router.urls