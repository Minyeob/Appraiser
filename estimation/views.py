from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import *
from estimation.models import Bookmark
#  파일을 import 할 때 from 에서 .을 이용하면 파일경로를 전부 칠 필요없이 현재 파일이 속한 파일의 다른 파일들을 가져올 수 있다
from .forms import UploadFileForm
from .models import Document
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext

# Create your views here.

class Bookmark_ListView(ListView):
    model = Bookmark

def upload_file(request):
    if request.method == 'POST':
        form=UploadFileForm(request.POST, request.FILES)

        #자신이 만든 폼의 필드는 기본값으로 required=true 로 되어 있으므로 모든 필드가 입력되지 않으면 유효하지 않다
        if form.is_valid():
            new_document=Document(file=request.FILES['file'])
            new_document.save()

            #reverse를 이용해서 http response를 해줄때는 urls.py 에 정의한 name을 이용해서 간편하게 원하는 주소로 redirect 시켜준다.
            return HttpResponseRedirect(reverse_lazy('estimation:upload'))

    else:
        form=UploadFileForm()
    documents = Document.objects.all()


    return render(request,'estimation/upload_file.html',{'documents':documents, 'form':form})