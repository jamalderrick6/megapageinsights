from django.urls import path, re_path
from .views import UrlsView, AddDomainView

urlpatterns = [
    path("domain/add", AddDomainView.as_view(), name="add a domain"),
    re_path("urls/(?P<domain_id>\d+)", UrlsView.as_view(), name="list domain urls"),
]
