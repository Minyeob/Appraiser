from django.conf.urls import url
from estimation.views import *
from . import views

urlpatterns = [
    url(r'^main/', Bookmark_ListView.as_view(), name='index'),
    url(r'^upload/', upload_file, name='upload')
]