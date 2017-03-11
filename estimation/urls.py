from django.conf.urls import url
from estimation.views import *
from . import views

urlpatterns = [
    url(r'^main/', Bookmark_ListView.as_view(), name='index'),
    url(r'^upload/', upload_file, name='upload'),
    # ?p<parameter 이름>파라미터 값 형태로 url을 통해 파라미터를 넘길 수 있다
    url(r'page/(?P<code>R(\d+)-(\d+))/', show_normal_report, name='page')
]