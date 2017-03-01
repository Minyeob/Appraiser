from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import *
from estimation.models import Bookmark
#  파일을 import 할 때 from 에서 .을 이용하면 파일경로를 전부 칠 필요없이 현재 파일이 속한 파일의 다른 파일들을 가져올 수 있다
from .forms import UploadFileForm
from .models import Document
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from .functiom import *
import xlrd
from django import shortcuts


# Create your views here.

class Bookmark_ListView(ListView):
    model = Bookmark

def upload_file(request):
    if request.method == 'POST':
        form=UploadFileForm(request.POST, request.FILES)

        #자신이 만든 폼의 필드는 기본값으로 required=true 로 되어 있으므로 모든 필드가 입력되지 않으면 유효하지 않다
        if form.is_valid():
            new_document=Document(file=request.FILES['file'])
            new_document.title=new_document.file.name
            worksheet =excel_handling().make_file(new_document.file)
            normal_datas=excel_handling().get_normal(worksheet)
            normal_codes=excel_handling().get_code_normal(worksheet)
            normals=zip(normal_datas, normal_codes)
            file=Document.objects.filter(title=new_document.title)
            if(len(file)==0):
                new_document.save()

            return render(request,'estimation/code_selection.html', {'normals':normals, 'file':new_document})

    else:
        form=UploadFileForm()
    documents = Document.objects.all()


    return render(request,'estimation/upload_file.html',{'documents':documents, 'form':form})

def show_normal_report(request, code):
    name=request.GET['title']
    file=Document.objects.get(title=name)
    worksheet = excel_handling().make_file(file.file)
    creditors=excel_handling().get_creditor(worksheet)

    return render(request, 'estimation/normal_report.html',{'code':code,'creditors':creditors})
