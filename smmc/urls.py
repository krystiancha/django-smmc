from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tags/', views.TagList.as_view()),
    url(r'^entries/tag/(?P<tag>\w+)/$', views.EntryViewSet.as_view({'get': 'tag'})),
    url(r'^entries/random/$', views.EntryViewSet.as_view({'get': 'random'})),
]
